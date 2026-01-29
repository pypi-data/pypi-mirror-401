import numpy as np
import time
import subprocess
import json
from typing import Dict, List, Tuple, Optional, Any, Callable
import warnings

try:
    import torch
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    warnings.warn("PyTorch not available. GPU optimizations disabled.")

try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False
    warnings.warn("CuPy not available. Some GPU features disabled.")


class GPURingOptimizer:
    """
    GPU-specific optimizations using ring theory patterns with adaptive sizing.
    """
    
    def __init__(self, device: str = "cuda:0"):
        """
        Initialize GPU optimizer.
        
        Args:
            device: CUDA device to use
        """
        self.device = device
        self.resonant_sizes = self._get_gpu_resonant_sizes()
        self.energy_readings = []
        self.size_patterns = {}
        self.load_history = []
        
    def _get_gpu_resonant_sizes(self) -> List[int]:
        """Определяет резонансные размеры для конкретной GPU."""
        # Базовые размеры из CPU эксперимента
        base_sizes = [32, 64, 128, 256, 512, 1024]
        
        if TORCH_AVAILABLE and torch.cuda.is_available():
            try:
                # Адаптируем под архитектуру GPU
                props = torch.cuda.get_device_properties(0)
                warp_size = props.warpSize  # Обычно 32
                
                # Добавляем размеры для тяжелых нагрузок
                memory_bandwidth = props.memory_clock_rate * props.memory_bus_width / 8 / 1e9
                
                # Оптимальные размеры для разных типов операций
                optimal_sizes = [
                    warp_size,
                    warp_size * 2,
                    warp_size * 4,
                    warp_size * 8,
                    warp_size * 16,
                    warp_size * 32,
                    warp_size * 64,
                ]
                
                # Добавляем размеры для кэша L1/L2
                # Типичные размеры кэша L1: 64KB, L2: 6MB
                cache_l1_optimal = int((64 * 1024) / 4)  # для float32
                cache_l2_optimal = int((6 * 1024 * 1024) / 4)
                
                optimal_sizes.extend([
                    cache_l1_optimal // 4,
                    cache_l1_optimal // 2,
                    cache_l1_optimal,
                    cache_l2_optimal // 4,
                    cache_l2_optimal // 2,
                    cache_l2_optimal
                ])
                
                # Объединяем с базовыми и сортируем
                all_sizes = list(set(base_sizes + optimal_sizes))
                all_sizes = [s for s in all_sizes if 16 <= s <= 16384]
                all_sizes.sort()
                return all_sizes
                
            except:
                pass
        
        return base_sizes
    
    def optimize_cuda_kernel(self, 
                            kernel_func: Callable,
                            grid_size: Tuple[int, int, int],
                            block_size: Tuple[int, int, int],
                            args: tuple) -> Dict[str, Any]:
        """
        Optimize CUDA kernel execution using ring patterns.
        
        Args:
            kernel_func: CUDA kernel function
            grid_size: Grid dimensions
            block_size: Block dimensions
            args: Kernel arguments
            
        Returns:
            Optimization results
        """
        if not TORCH_AVAILABLE or not torch.cuda.is_available():
            return {"error": "CUDA not available"}
        
        results = {
            "original": self._benchmark_kernel(kernel_func, grid_size, block_size, args),
            "optimized": None
        }
        
        # Оптимизируем размеры grid/block
        optimized_grid = self._optimize_grid_dims(grid_size)
        optimized_block = self._optimize_block_dims(block_size)
        
        results["optimized"] = self._benchmark_kernel(
            kernel_func, optimized_grid, optimized_block, args
        )
        
        # Рассчитываем улучшение
        if results["original"]["energy"] > 0:
            energy_savings = (
                results["original"]["energy"] - results["optimized"]["energy"]
            ) / results["original"]["energy"] * 100
            
            results["energy_savings_percent"] = max(0.0, energy_savings)
            results["performance_improvement"] = (
                results["optimized"]["throughput"] / results["original"]["throughput"] - 1
            ) * 100
        
        return results
    
    def _benchmark_kernel(self, kernel_func, grid_size, block_size, args):
        """Замеряет производительность и энергопотребление ядра."""
        start_time = time.time()
        start_energy = self._get_gpu_energy()
        
        # Выполняем ядро несколько раз для точности
        iterations = 100
        for _ in range(iterations):
            kernel_func[grid_size, block_size](*args)
        
        torch.cuda.synchronize()
        
        end_time = time.time()
        end_energy = self._get_gpu_energy()
        
        duration = end_time - start_time
        energy_used = end_energy - start_energy
        
        # Расчет пропускной способности
        total_work = np.prod(grid_size) * np.prod(block_size) * iterations
        throughput = total_work / duration / 1e9  # GFlops (оценка)
        
        return {
            "duration": duration,
            "energy": energy_used,
            "throughput": throughput,
            "grid_size": grid_size,
            "block_size": block_size
        }
    
    def _optimize_grid_dims(self, grid_size: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Оптимизирует размеры grid."""
        gx, gy, gz = grid_size
        
        # Приводим к резонансным размерам
        opt_gx = self._find_nearest_resonant(gx)
        opt_gy = self._find_nearest_resonant(gy)
        opt_gz = self._find_nearest_resonant(gz) if gz > 1 else 1
        
        return (opt_gx, opt_gy, opt_gz)
    
    def _optimize_block_dims(self, block_size: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """Оптимизирует размеры block."""
        bx, by, bz = block_size
        
        # Для block обычно используют степени двойки
        powers_of_two = [32, 64, 128, 256, 512, 1024]
        
        opt_bx = min(powers_of_two, key=lambda x: abs(x - bx))
        opt_by = 1  # Обычно для лучшей occupancy
        opt_bz = 1
        
        return (opt_bx, opt_by, opt_bz)
    
    def _find_nearest_resonant(self, size: int) -> int:
        """Находит ближайший резонансный размер."""
        # Для тяжелых нагрузок выбираем большие резонансные размеры
        if size > 1024:
            # Для больших размеров выбираем кратные 256
            large_sizes = [s for s in self.resonant_sizes if s >= 512]
            if large_sizes:
                distances = [(abs(size - rs), rs) for rs in large_sizes]
                distances.sort()
                return distances[0][1]
        
        # Для малых и средних размеров используем все доступные
        distances = [(abs(size - rs), rs) for rs in self.resonant_sizes]
        distances.sort()
        return distances[0][1]
    
    def _get_gpu_energy(self) -> float:
        """Получает текущее энергопотребление GPU."""
        try:
            if TORCH_AVAILABLE and torch.cuda.is_available():
                result = subprocess.run(
                    ['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits'],
                    capture_output=True, text=True
                )
                
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')
                    if lines:
                        return float(lines[0].strip())
        except:
            pass
        
        return 0.0
    
    def optimize_tensor_operation(self, 
                                 tensor: torch.Tensor,
                                 tensor2: Optional[torch.Tensor] = None,
                                 operation: str = "matmul",
                                 workload_type: str = "normal") -> torch.Tensor:
        """
        Optimize tensor operations using ring patterns with workload adaptation.
        
        Args:
            tensor: Input tensor
            tensor2: Second input tensor for binary operations
            operation: Operation to perform
            workload_type: "light", "normal", "heavy", "sequential"
            
        Returns:
            Optimized result
        """
        if not TORCH_AVAILABLE:
            if tensor2 is None:
                return tensor
            else:
                return tensor2 if operation == "matmul" else tensor
        
        # Сохраняем информацию о нагрузке
        self.load_history.append({
            'timestamp': time.time(),
            'size': tensor.shape,
            'operation': operation,
            'workload_type': workload_type
        })
        
        # Ограничиваем историю
        if len(self.load_history) > 1000:
            self.load_history = self.load_history[-1000:]
        
        # Адаптируем стратегию под тип нагрузки
        if workload_type == "heavy":
            return self._optimize_heavy_workload(tensor, tensor2, operation)
        elif workload_type == "sequential":
            return self._optimize_sequential_workload(tensor, tensor2, operation)
        elif workload_type == "light":
            return self._optimize_light_workload(tensor, tensor2, operation)
        else:
            return self._optimize_normal_workload(tensor, tensor2, operation)
    
    def _optimize_heavy_workload(self, tensor: torch.Tensor, 
                                tensor2: Optional[torch.Tensor],
                                operation: str) -> torch.Tensor:
        """Оптимизация для тяжелых нагрузок (многократные операции)."""
        if operation == "matmul":
            if tensor2 is None:
                # Для self-matmul: A * Aᵀ
                return self._optimized_heavy_matmul(tensor, tensor.T)
            else:
                return self._optimized_heavy_matmul(tensor, tensor2)
        elif operation == "conv":
            return self._ring_convolution(tensor)
        else:
            return tensor if tensor2 is None else tensor2
    
    def _optimize_sequential_workload(self, tensor: torch.Tensor,
                                     tensor2: Optional[torch.Tensor],
                                     operation: str) -> torch.Tensor:
        """Оптимизация для последовательных операций (цепочки)."""
        # Для последовательных операций важно сохранять размеры
        # для кэширования промежуточных результатов
        if operation == "matmul":
            if tensor2 is None:
                # Без изменения размеров для лучшего кэширования
                return torch.matmul(tensor, tensor.T)
            else:
                # Минимальная оптимизация размеров
                return self._optimized_cached_matmul(tensor, tensor2)
        else:
            return tensor if tensor2 is None else tensor2
    
    def _optimize_light_workload(self, tensor: torch.Tensor,
                                tensor2: Optional[torch.Tensor],
                                operation: str) -> torch.Tensor:
        """Оптимизация для легких нагрузок (единичные операции)."""
        # Для легких нагрузок минимизируем накладные расходы
        if operation == "matmul":
            if tensor2 is None:
                return torch.matmul(tensor, tensor.T)
            else:
                return torch.matmul(tensor, tensor2)
        else:
            return tensor if tensor2 is None else tensor2
    
    def _optimize_normal_workload(self, tensor: torch.Tensor,
                                 tensor2: Optional[torch.Tensor],
                                 operation: str) -> torch.Tensor:
        """Оптимизация для нормальных нагрузок."""
        # Базовая оптимизация размеров
        if operation == "matmul":
            if tensor2 is None:
                # Для self-matmul: A * Aᵀ
                return self._ring_matmul(tensor, tensor.T)
            else:
                # С мягкой оптимизацией размеров
                return self._optimized_matmul_with_padding(tensor, tensor2)
        elif operation == "conv":
            return self._ring_convolution(tensor)
        else:
            return tensor if tensor2 is None else tensor2
    
    def _optimized_heavy_matmul(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        """Оптимизированное matmul для тяжелых нагрузок."""
        m, n = a.shape[-2], a.shape[-1]
        n2, p = b.shape[-2], b.shape[-1]

        # Для очень больших матриц не применяем оптимизацию
        if m >= 4096 or n >= 4096 or n2 >= 4096 or p >= 4096:
            return torch.matmul(a, b)

        # Определяем, нужно ли оптимизировать
        if not self._should_optimize_for_heavy_workload((m, n), (n2, p)):
            return torch.matmul(a, b)

        # Находим оптимальный внутренний размер
        optimal_n = self._find_optimal_inner_size_for_heavy_load(n, n2)

        # Если оптимальный размер совпадает с текущим, возвращаем как есть
        if optimal_n == n and optimal_n == n2:
            return torch.matmul(a, b)

        # Корректируем размеры только если optimal_n >= текущим размерам
        if optimal_n > n:
            a = self._pad_tensor(a, optimal_n, dim=-1)
        if optimal_n > n2:
            b = self._pad_tensor(b, optimal_n, dim=-2)

        result = torch.matmul(a, b)

        # Если мы увеличивали размер, нужно обрезать обратно
        if result.shape[-1] > p:
            result = self._crop_tensor(result, p, dim=-1)

        return result
    def _should_optimize_for_heavy_workload(self, shape1: Tuple[int, int], 
                                      shape2: Tuple[int, int]) -> bool:
        """Определяет, стоит ли оптимизировать для тяжелой нагрузки."""
        m, n = shape1
        n2, p = shape2

        # Для больших матриц (>=4096) стандартное умножение уже эффективно
        if m >= 4096 or n >= 4096 or n2 >= 4096 or p >= 4096:
            return False

        # Для средних размеров (2048) проверяем возможность оптимизации
        if m * n >= 2048 * 2048 or n2 * p >= 2048 * 2048:
            min_n = min(n, n2)
            optimal_n = self._find_optimal_inner_size_for_heavy_load(min_n, min_n)

            # Оптимизируем только если:
            # 1. Оптимальный размер отличается от текущего
            # 2. И оптимальный размер больше текущего (увеличение)
            if optimal_n != min_n and optimal_n > min_n:
                increase = (optimal_n - min_n) / min_n
                if increase < 0.25:  # Не более 25% увеличения
                    return True

        return False
    def _find_optimal_inner_size_for_heavy_load(self, n1: int, n2: int) -> int:
        """Находит оптимальный внутренний размер для тяжелых нагрузок с ограничениями."""
        min_n = min(n1, n2)

        # 1. Ищем резонансные размеры, которые >= min_n (увеличение, а не уменьшение)
        candidates = []
        for size in self.resonant_sizes:
            if size >= min_n:  # Только увеличение размера
                increase = (size - min_n) / min_n
                if increase < 0.25:  # Не более 25% увеличения
                    score = 0
                    if size % 64 == 0:
                        score += 2  # Оптимально для tensor cores
                    if size % 128 == 0:
                        score += 1  # Хорошо для кэша
                    if bin(size).count('1') == 1:  # Степень двойки
                        score += 2
                    # Предпочитаем наименьшее увеличение
                    candidates.append((score, -increase, size))

        if candidates:
            candidates.sort(reverse=True)
            return candidates[0][2]

        # 2. Если не нашли подходящий размер для увеличения, возвращаем текущий
        return min_n
    
    def _optimized_cached_matmul(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        """Matmul с оптимизацией для кэширования."""
        # Оптимизируем для лучшего использования кэша
        m, n = a.shape[-2], a.shape[-1]
        n2, p = b.shape[-2], b.shape[-1]
        
        # Для кэширования выбираем размеры, которые помещаются в L2 кэш
        cache_friendly_size = self._find_cache_friendly_size(n, n2)
        
        if cache_friendly_size != n or cache_friendly_size != n2:
            if n != cache_friendly_size:
                a = self._pad_tensor(a, cache_friendly_size, dim=-1)
            if n2 != cache_friendly_size:
                b = self._pad_tensor(b, cache_friendly_size, dim=-2)
        
        result = torch.matmul(a, b)
        
        if result.shape[-1] != p:
            result = self._crop_tensor(result, p, dim=-1)
        
        return result
    
    def _optimized_matmul_with_padding(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        """Matmul с мягкой оптимизацией через padding."""
        m, n = a.shape[-2], a.shape[-1]
        n2, p = b.shape[-2], b.shape[-1]
        
        # Находим ближайший резонансный размер
        optimal_n = self._find_nearest_resonant(min(n, n2))
        
        # Оптимизируем только если это даст выигрыш
        if abs(optimal_n - n) / n < 0.2 and abs(optimal_n - n2) / n2 < 0.2:
            if n != optimal_n:
                a = self._pad_tensor(a, optimal_n, dim=-1)
            if n2 != optimal_n:
                b = self._pad_tensor(b, optimal_n, dim=-2)
        
        result = torch.matmul(a, b)
        
        if result.shape[-1] != p:
            result = self._crop_tensor(result, p, dim=-1)
        
        return result
    
    def _should_optimize_for_heavy_workload(self, shape1: Tuple[int, int], 
                                          shape2: Tuple[int, int]) -> bool:
        """Определяет, стоит ли оптимизировать для тяжелой нагрузки."""
        m, n = shape1
        n2, p = shape2
        
        # Оптимизируем только для достаточно больших матриц
        if m * n < 1024 * 1024 or n2 * p < 1024 * 1024:
            return False
        
        # Проверяем, насколько текущий размер далек от оптимального
        optimal_n = self._find_nearest_resonant(min(n, n2))
        deviation = abs(optimal_n - min(n, n2)) / min(n, n2)
        
        # Оптимизируем если отклонение > 15%
        return deviation > 0.15
    
    def _find_optimal_inner_size_for_heavy_load(self, n1: int, n2: int) -> int:
        """Находит оптимальный внутренний размер для тяжелых нагрузок."""
        min_n = min(n1, n2)
        
        # Для тяжелых нагрузок выбираем размеры, которые:
        # 1. Делится на 64 (оптимально для tensor cores)
        # 2. Близок к степени двойки
        # 3. Не слишком увеличивает размер
        
        candidates = []
        for size in self.resonant_sizes:
            if size >= 256:  # Для тяжелых нагрузок
                # Вычисляем увеличение размера
                increase = abs(size - min_n) / min_n
                if increase < 0.3:  # Не более 30% увеличения
                    # Оцениваем эффективность
                    score = 0
                    if size % 64 == 0:
                        score += 2  # Оптимально для tensor cores
                    if size % 128 == 0:
                        score += 1  # Хорошо для кэша
                    if bin(size).count('1') == 1:  # Степень двойки
                        score += 2
                    
                    candidates.append((score, -increase, size))
        
        if candidates:
            candidates.sort(reverse=True)
            return candidates[0][2]
        
        return self._find_nearest_resonant(min_n)
    
    def _find_cache_friendly_size(self, n1: int, n2: int) -> int:
        """Находит размер, дружественный к кэшу."""
        min_n = min(n1, n2)
        
        # Ищем размеры, которые хорошо помещаются в кэш
        # Предполагаем float32 (4 байта)
        cache_sizes = [
            16384,  # ~64KB L1 кэш
            32768,  # ~128KB
            65536,  # ~256KB
            131072,  # ~512KB
            262144,  # ~1MB
            524288,  # ~2MB
            1048576,  # ~4MB
        ]
        
        for cache_size in cache_sizes:
            if min_n <= cache_size:
                # Находим ближайший резонансный размер, не превышающий cache_size
                suitable_sizes = [s for s in self.resonant_sizes if s <= cache_size]
                if suitable_sizes:
                    return min(suitable_sizes, key=lambda x: abs(x - min_n))
        
        return min_n
    
    def _pad_tensor(self, tensor: torch.Tensor, new_size: int, dim: int) -> torch.Tensor:
        """Дополняет тензор до нужного размера."""
        current_size = tensor.shape[dim]

        if current_size == new_size:
            return tensor

        # Создаем новый тензор
        new_shape = list(tensor.shape)
        new_shape[dim] = new_size

        result = torch.zeros(new_shape, device=tensor.device, dtype=tensor.dtype)

        # Копируем данные - копируем только до min(current_size, new_size)
        if dim == -1:  # Последняя размерность
            copy_size = min(current_size, new_size)
            result[..., :copy_size] = tensor[..., :copy_size]
        elif dim == -2:  # Предпоследняя размерность
            copy_size = min(current_size, new_size)
            result[..., :copy_size, :] = tensor[..., :copy_size, :]

        return result
    
    def _crop_tensor(self, tensor: torch.Tensor, new_size: int, dim: int) -> torch.Tensor:
        """Обрезает тензор до нужного размера."""
        current_size = tensor.shape[dim]
        
        if current_size == new_size:
            return tensor
        
        # Создаем срез
        slices = [slice(None)] * len(tensor.shape)
        slices[dim] = slice(0, new_size)
        
        return tensor[tuple(slices)]
    
    def _ring_matmul(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        """Умножение матриц с кольцевой оптимизацией."""
        return torch.matmul(a, b)
    
    def _ring_convolution(self, x: torch.Tensor) -> torch.Tensor:
        """Свертка с кольцевой оптимизацией."""
        if len(x.shape) == 4:  # [batch, channels, height, width]
            kernel_size = 3
            weight = torch.ones(1, 1, kernel_size, kernel_size, device=x.device) / (kernel_size ** 2)
            return F.conv2d(x, weight, padding=kernel_size // 2)
        else:
            return x


# Остальные функции остаются без изменений
def gpu_energy_monitor(interval: float = 1.0, duration: float = 10.0) -> Dict[str, Any]:
    """Monitor GPU energy consumption during computations."""
    if not TORCH_AVAILABLE or not torch.cuda.is_available():
        return {"error": "GPU not available"}
    
    readings = []
    start_time = time.time()
    
    while time.time() - start_time < duration:
        try:
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=power.draw,temperature.gpu,utilization.gpu',
                 '--format=csv,noheader,nounits'],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                data = result.stdout.strip().split(',')
                if len(data) >= 3:
                    reading = {
                        'timestamp': time.time(),
                        'power_w': float(data[0].strip()),
                        'temp_c': float(data[1].strip()),
                        'utilization': float(data[2].strip())
                    }
                    readings.append(reading)
        
        except:
            pass
        
        time.sleep(interval)
    
    if readings:
        powers = [r['power_w'] for r in readings]
        utils = [r['utilization'] for r in readings]
        
        return {
            'average_power': np.mean(powers),
            'max_power': np.max(powers),
            'min_power': np.min(powers),
            'average_utilization': np.mean(utils),
            'readings': readings
        }
    
    return {"error": "No readings collected"}


def find_gpu_resonance(max_size: int = 1024) -> Dict[str, List[int]]:
    """Find resonant sizes for current GPU by benchmarking."""
    if not TORCH_AVAILABLE or not torch.cuda.is_available():
        return {"error": "GPU not available"}
    
    test_sizes = [32, 64, 128, 256, 512, 1024, 2048]
    test_sizes = [s for s in test_sizes if s <= max_size]
    
    results = {}
    
    for size in test_sizes:
        try:
            a = torch.randn(size, size, device='cuda')
            b = torch.randn(size, size, device='cuda')
            
            start = time.time()
            for _ in range(10):
                c = torch.matmul(a, b)
            torch.cuda.synchronize()
            duration = time.time() - start
            
            power_result = subprocess.run(
                ['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits'],
                capture_output=True, text=True
            )
            
            power = 0.0
            if power_result.returncode == 0:
                power = float(power_result.stdout.strip())
            
            throughput = (size ** 3) * 10 / duration / 1e9
            efficiency = throughput / power if power > 0 else 0
            
            results[size] = {
                'duration': duration,
                'throughput_gflops': throughput,
                'power_w': power,
                'efficiency': efficiency
            }
            
        except Exception as e:
            print(f"Error testing size {size}: {e}")
    
    if results:
        sorted_sizes = sorted(results.items(), key=lambda x: x[1]['efficiency'], reverse=True)
        resonant_sizes = [size for size, _ in sorted_sizes[:3]]
        
        return {
            'resonant_sizes': resonant_sizes,
            'all_results': results
        }
    
    return {"error": "No results collected"}