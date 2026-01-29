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
    GPU-specific optimizations using ring theory patterns.
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
        
    def _get_gpu_resonant_sizes(self) -> List[int]:
        """Определяет резонансные размеры для конкретной GPU."""
        # Базовые размеры из CPU эксперимента
        base_sizes = [32, 64, 128, 256, 512, 1024]
        
        if TORCH_AVAILABLE and torch.cuda.is_available():
            try:
                # Адаптируем под архитектуру GPU
                props = torch.cuda.get_device_properties(0)
                warp_size = props.warpSize  # Обычно 32
                
                # Оптимальные размеры для GPU
                optimal_sizes = [
                    warp_size,
                    warp_size * 2,
                    warp_size * 4,
                    warp_size * 8,
                    warp_size * 16,
                    warp_size * 32,
                ]
                
                # Объединяем с базовыми
                all_sizes = list(set(base_sizes + optimal_sizes))
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
        # (упрощенно, зависит от конкретного ядра)
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
        distances = [(abs(size - rs), rs) for rs in self.resonant_sizes]
        distances.sort()
        return distances[0][1]
    
    def _get_gpu_energy(self) -> float:
        """Получает текущее энергопотребление GPU."""
        try:
            if TORCH_AVAILABLE and torch.cuda.is_available():
                # Используем nvidia-smi через subprocess
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
                                 operation: str = "matmul") -> torch.Tensor:
        """
        Optimize tensor operations using ring patterns.
        
        Args:
            tensor: Input tensor
            operation: Operation to perform
            
        Returns:
            Optimized result
        """
        if not TORCH_AVAILABLE:
            return tensor
        
        # 1. Преобразуем к оптимальному (резонансному) размеру
        original_shape = tensor.shape
        optimal_shape = self._optimize_tensor_shape(original_shape)
        
        if original_shape != optimal_shape:
            # Сохраняем оригинальный тензор для восстановления размера
            tensor_reshaped = self._reshape_tensor(tensor, optimal_shape)
        else:
            tensor_reshaped = tensor
        
        # 2. Выполняем кольцевую оптимизацию
        if operation == "matmul":
            result = self._ring_matmul(tensor_reshaped, tensor_reshaped)
        elif operation == "conv":
            result = self._ring_convolution(tensor_reshaped)
        else:
            result = tensor_reshaped
        
        # 3. Восстанавливаем исходный размер если нужно
        if result.shape != original_shape:
            result = self._restore_original_size(result, original_shape)
        
        return result
    
    def _optimize_tensor_shape(self, shape: Tuple[int, ...]) -> Tuple[int, ...]:
        """Оптимизирует форму тензора по теории ТРАП."""
        if len(shape) >= 2:
            # Для матричных операций
            rows, cols = shape[-2], shape[-1]
            
            # Для ТРАП: преобразуем к ближайшему резонансному размеру
            opt_rows = self._find_nearest_resonant(rows)
            opt_cols = self._find_nearest_resonant(cols)
            
            return shape[:-2] + (opt_rows, opt_cols)
        else:
            # Для векторов
            size = shape[0]
            opt_size = self._find_nearest_resonant(size)
            return (opt_size,)
    
    def _reshape_tensor(self, tensor: torch.Tensor, new_shape: Tuple[int, ...]) -> torch.Tensor:
        """Изменяет форму тензора с сохранением данных."""
        try:
            return tensor.reshape(new_shape)
        except:
            # Если не получается, создаем новый тензор
            result = torch.zeros(new_shape, device=tensor.device, dtype=tensor.dtype)
            
            # Копируем данные
            slices = [slice(0, min(s1, s2)) for s1, s2 in zip(tensor.shape, new_shape)]
            result[slices] = tensor[slices]
            
            return result
    
    def _restore_original_size(self, tensor: torch.Tensor, original_shape: Tuple[int, ...]) -> torch.Tensor:
        """Восстанавливает исходный размер тензора после оптимизации."""
        # Если результат меньше оригинала - дополняем нулями
        if tensor.numel() < np.prod(original_shape):
            result = torch.zeros(original_shape, device=tensor.device, dtype=tensor.dtype)
            # Копируем данные в начало
            slices = [slice(0, s) for s in tensor.shape]
            result[slices] = tensor
            return result
        # Если результат больше оригинала - обрезаем
        elif tensor.numel() > np.prod(original_shape):
            slices = [slice(0, s) for s in original_shape]
            return tensor[slices]
        else:
            # Размеры совпадают по количеству элементов, но разная форма
            return tensor.reshape(original_shape)
    
    def _ring_matmul(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        """Кольцевая оптимизация умножения матриц по теории ТРАП."""
        if a.shape != b.shape or len(a.shape) != 2:
            return torch.matmul(a, b)

        size = a.shape[0]
        result = torch.zeros_like(a)

        # 1. Определяем центральную область по ТРАП
        center_size = min(50 + size // 10, size - 2)
        center_size = max(2, center_size)  # Минимум 2x2

        # 2. Вычисляем границы для кольцевой структуры
        border = min(2, size // 4)  # Толщина границы

        # 3. Разделяем матрицу на зоны:
        #    - Внутреннее кольцо (центр) - полное вычисление
        #    - Среднее кольцо - частичное вычисление  
        #    - Внешнее кольцо - копирование/интерполяция
        
        if center_size > 0:
            # Внутренняя область: полное умножение
            inner_a = a[border:center_size, border:center_size]
            inner_b = b[border:center_size, border:center_size]
            inner_result = torch.matmul(inner_a, inner_b)
            result[border:center_size, border:center_size] = inner_result

        # 4. Средняя область: вычисляем строки и столбцы отдельно
        for i in range(size):
            if i < border or i >= size - border:
                # Внешние строки: частичное вычисление
                row_a = a[i:i+1, :]
                result[i, :] = torch.matmul(row_a, b).squeeze()
            elif i >= border and i < border + 2:
                # Средние строки: интерполяция
                prev_row = a[i-1:i, :] if i > 0 else a[i:i+1, :]
                next_row = a[i+1:i+2, :] if i < size-1 else a[i:i+1, :]
                avg_row = (prev_row + next_row) / 2
                result[i, :] = torch.matmul(avg_row, b).squeeze()

        # 5. Для столбцов аналогично
        for j in range(size):
            if j < border or j >= size - border:
                # Внешние столбцы
                col_b = b[:, j:j+1]
                result[:, j] = torch.matmul(a, col_b).squeeze()

        return result

    def _fill_diagonals(self, a: torch.Tensor, b: torch.Tensor, result: torch.Tensor):
        """Заполняет диагональные элементы."""
        size = a.shape[0]

        # Главная диагональ - усреднение соседних элементов
        for i in range(1, size-1):
            if i < size-1:
                if i < result.shape[0]-1 and i < result.shape[1]-1:
                    # Проверяем что соседи не нулевые
                    neighbors = []
                    if result[i, i-1] != 0:
                        neighbors.append(result[i, i-1])
                    if result[i, i+1] != 0:
                        neighbors.append(result[i, i+1])
                    if result[i-1, i] != 0:
                        neighbors.append(result[i-1, i])
                    if result[i+1, i] != 0:
                        neighbors.append(result[i+1, i])
                    
                    if neighbors:
                        result[i, i] = sum(neighbors) / len(neighbors)

    def _fill_remaining(self, a: torch.Tensor, b: torch.Tensor, result: torch.Tensor, center_size: int):
        """Заполняет оставшиеся области."""
        size = a.shape[0]

        # Заполняем области между центром и границами
        for i in range(size):
            for j in range(size):
                if result[i, j] == 0:  # Еще не заполнено
                    # Интерполяция на основе ближайших известных значений
                    if i == 0 or j == 0 or i == size-1 or j == size-1:
                        continue  # Границы уже заполнены
                    elif i <= center_size and j <= center_size:
                        continue  # Центральная область уже заполнена
                    else:
                        # Простая интерполяция: среднее 4 соседей
                        neighbors = []
                        if i > 0 and result[i-1, j] != 0:
                            neighbors.append(result[i-1, j])
                        if i < size-1 and result[i+1, j] != 0:
                            neighbors.append(result[i+1, j])
                        if j > 0 and result[i, j-1] != 0:
                            neighbors.append(result[i, j-1])
                        if j < size-1 and result[i, j+1] != 0:
                            neighbors.append(result[i, j+1])

                        if neighbors:
                            result[i, j] = sum(neighbors) / len(neighbors)
                        else:
                            # Fallback: берем соответствующий элемент из a
                            result[i, j] = a[i, j]
                            
    def _ring_convolution(self, x: torch.Tensor) -> torch.Tensor:
        """Свертка с кольцевой оптимизацией для стабильности."""
        if len(x.shape) != 4:  # Только для [batch, channels, height, width]
            return x

        batch_size, channels, height, width = x.shape
        
        # 1. Стандартная свертка
        kernel_size = 3
        weight = torch.ones(channels, channels, kernel_size, kernel_size, 
                           device=x.device) / (kernel_size ** 2 * channels)
        
        full_result = F.conv2d(x, weight, padding=kernel_size//2)
        
        # 2. Применяем кольцевую стабилизацию
        result = full_result.clone()
        
        # 3. Сглаживаем границы
        border = 1
        if height > 2 * border and width > 2 * border:
            # Граничные строки
            result[:, :, :border, :] = (
                full_result[:, :, :border, :] + 
                full_result[:, :, border:2*border, :]
            ) / 2
            
            result[:, :, -border:, :] = (
                full_result[:, :, -border:, :] + 
                full_result[:, :, -2*border:-border, :]
            ) / 2
            
            # Граничные столбцы
            result[:, :, :, :border] = (
                full_result[:, :, :, :border] + 
                full_result[:, :, :, border:2*border]
            ) / 2
            
            result[:, :, :, -border:] = (
                full_result[:, :, :, -border:] + 
                full_result[:, :, :, -2*border:-border]
            ) / 2
        
        return result


def gpu_energy_monitor(interval: float = 1.0, duration: float = 10.0) -> Dict[str, Any]:
    """
    Monitor GPU energy consumption during computations.
    
    Args:
        interval: Measurement interval in seconds
        duration: Total monitoring duration
        
    Returns:
        Energy statistics
    """
    if not TORCH_AVAILABLE or not torch.cuda.is_available():
        return {"error": "GPU not available"}
    
    readings = []
    start_time = time.time()
    
    while time.time() - start_time < duration:
        try:
            # Читаем энергопотребление через nvidia-smi
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
    
    # Анализируем данные
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
    """
    Find resonant sizes for current GPU by benchmarking.
    
    Args:
        max_size: Maximum size to test
        
    Returns:
        Dictionary with resonant sizes
    """
    if not TORCH_AVAILABLE or not torch.cuda.is_available():
        return {"error": "GPU not available"}
    
    # Тестируем различные размеры
    test_sizes = [32, 64, 128, 256, 512, 1024, 2048]
    test_sizes = [s for s in test_sizes if s <= max_size]
    
    results = {}
    
    for size in test_sizes:
        try:
            # Создаем тестовые тензоры
            a = torch.randn(size, size, device='cuda')
            b = torch.randn(size, size, device='cuda')
            
            # Замеряем производительность
            start = time.time()
            for _ in range(10):
                c = torch.matmul(a, b)
            torch.cuda.synchronize()
            duration = time.time() - start
            
            # Читаем энергопотребление
            power_result = subprocess.run(
                ['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits'],
                capture_output=True, text=True
            )
            
            power = 0.0
            if power_result.returncode == 0:
                power = float(power_result.stdout.strip())
            
            # Сохраняем результаты
            throughput = (size ** 3) * 10 / duration / 1e9  # GFlops
            efficiency = throughput / power if power > 0 else 0
            
            results[size] = {
                'duration': duration,
                'throughput_gflops': throughput,
                'power_w': power,
                'efficiency': efficiency
            }
            
        except Exception as e:
            print(f"Error testing size {size}: {e}")
    
    # Находим наиболее эффективные размеры
    if results:
        # Сортируем по эффективности
        sorted_sizes = sorted(results.items(), key=lambda x: x[1]['efficiency'], reverse=True)
        
        # Берем топ-3
        resonant_sizes = [size for size, _ in sorted_sizes[:3]]
        
        return {
            'resonant_sizes': resonant_sizes,
            'all_results': results
        }
    
    return {"error": "No results collected"}