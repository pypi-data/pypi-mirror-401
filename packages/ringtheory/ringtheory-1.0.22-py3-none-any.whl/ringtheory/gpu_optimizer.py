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
    Based on ТРАП (Theory of Recursive Autopatterns) experimental results.
    """
    
    def __init__(self, device: str = "cuda:0"):
        """
        Initialize GPU optimizer with resonant sizes based on experiments.
        
        Args:
            device: CUDA device to use
        """
        self.device = device
        self.resonant_sizes = self._get_optimized_resonant_sizes()
        self.energy_readings = []
        
    def _get_optimized_resonant_sizes(self) -> List[int]:
        """Определяет оптимизированные резонансные размеры на основе экспериментов ТРАП."""
        # Из экспериментов: оптимальные размеры для кольцевых структур
        # N=200 показал лучшую стабильность и энергоэффективность
        
        # Резонансные размеры из экспериментов
        experimental_sizes = [25, 50, 100, 200, 400, 800]
        
        if TORCH_AVAILABLE and torch.cuda.is_available():
            try:
                props = torch.cuda.get_device_properties(0)
                warp_size = props.warpSize  # Обычно 32
                
                # Добавляем размеры, выровненные по warp
                warp_aligned = [warp_size * i for i in [1, 2, 4, 8, 16, 32]]
                
                # Объединяем и выбираем лучшие на основе экспериментов
                all_sizes = list(set(experimental_sizes + warp_aligned + [200, 400, 800]))
                all_sizes.sort()
                
                # Приоритет: размеры, показавшие хорошую стабильность в экспериментах
                priority_sizes = [200, 400, 100, 800, 50, 25]
                
                # Сортируем по приоритету
                optimized = []
                for ps in priority_sizes:
                    if ps in all_sizes:
                        optimized.append(ps)
                        all_sizes.remove(ps)
                
                # Добавляем остальные
                optimized.extend(all_sizes)
                return optimized
                
            except:
                pass
        
        return experimental_sizes
    
    def optimize_tensor_operation(
    self,
    a: torch.Tensor,
    b: Optional[torch.Tensor] = None,
    operation: str = "matmul"
) -> torch.Tensor:
        """
        Оптимизированные тензорные операции.
        """
        if not TORCH_AVAILABLE:
            return a

        if operation == "matmul":
            if b is None:
                # Умножение матрицы на саму себя
                if a.shape[0] != a.shape[1]:
                    # Для неквадратных матриц - используем A @ A.T
                    return self._ring_matmul(a, a.t())
                else:
                    return self._ring_self_matmul(a)
            else:
                return self._ring_matmul(a, b)

        raise NotImplementedError(f"Operation '{operation}' not supported")

    def _ring_self_matmul(self, a: torch.Tensor, block_size: int = 200) -> torch.Tensor:
        """
        КОРРЕКТНОЕ умножение матрицы на себя: C = A @ A

        Args:
            a: Tensor [N, N] (квадратная матрица)
            block_size: размер блока (200 - оптимально по ТРАП)

        Returns:
            Tensor [N, N]
        """
        assert a.dim() == 2, "Только 2D матрицы поддерживаются"
        assert a.shape[0] == a.shape[1], "Матрица должна быть квадратной"

        N = a.shape[0]
        device = a.device
        dtype = a.dtype

        # Результат
        c = torch.zeros((N, N), device=device, dtype=dtype)

        # Блоковое умножение
        for i in range(0, N, block_size):
            i_end = min(i + block_size, N)

            for j in range(0, N, block_size):
                j_end = min(j + block_size, N)

                # Блок результата
                block_result = torch.zeros(i_end - i, j_end - j, 
                                          device=device, dtype=dtype)

                # Внутренняя сумма по k
                for k in range(0, N, block_size):
                    k_end = min(k + block_size, N)

                    # Блоки A[i:i_end, k:k_end] × A[k:k_end, j:j_end]
                    block_a1 = a[i:i_end, k:k_end]
                    block_a2 = a[k:k_end, j:j_end]

                    block_result += torch.matmul(block_a1, block_a2)

                # Записываем блок в результат
                c[i:i_end, j:j_end] = block_result

        return c



    def _ring_matmul_square_fixed(self, a: torch.Tensor) -> torch.Tensor:
        """
        Умножение квадратной матрицы на себя.

        Args:
            a: Input matrix [N, N] (должна быть квадратной)

        Returns:
            Result matrix [N, N] (A × A)
        """
        if len(a.shape) != 2:
            raise ValueError(f"Expected 2D tensor, got shape {a.shape}")

        if a.shape[0] != a.shape[1]:
            raise ValueError(f"Expected square matrix, got shape {a.shape}")

        return self._ring_self_matmul(a)
    
    def _ring_matmul(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        """
        КОРРЕКТНОЕ блоковое умножение матриц A × B.
        """
        if a.ndim != 2 or b.ndim != 2:
            raise ValueError("Both inputs must be 2D tensors")

        M, K1 = a.shape
        K2, N = b.shape

        if K1 != K2:
            raise ValueError(f"Incompatible shapes: {a.shape} × {b.shape}")

        device = a.device
        dtype = a.dtype

        # Оптимальный размер блока из ТРАП экспериментов
        block_size = 200

        # Для маленьких матриц — стандартное умножение
        if M <= block_size and N <= block_size and K1 <= block_size:
            return torch.matmul(a, b)

        # Результат
        result = torch.zeros((M, N), device=device, dtype=dtype)

        # Блоковое умножение
        for i in range(0, M, block_size):
            i_end = min(i + block_size, M)

            for j in range(0, N, block_size):
                j_end = min(j + block_size, N)

                # Аккумулятор блока
                block_result = torch.zeros(
                    (i_end - i, j_end - j),
                    device=device,
                    dtype=dtype
                )

                for k in range(0, K1, block_size):
                    k_end = min(k + block_size, K1)

                    a_block = a[i:i_end, k:k_end]
                    b_block = b[k:k_end, j:j_end]

                    block_result += torch.matmul(a_block, b_block)

                result[i:i_end, j:j_end] = block_result

        return result

    
    def _match_shapes(self, tensor: torch.Tensor, target_shape: Tuple[int, ...]) -> torch.Tensor:
        """
        Приводит тензор к целевому размеру.
        Обрезает или дополняет нулями при необходимости.
        """
        if tensor.shape == target_shape:
            return tensor
        
        print(f"Matching shapes: {tensor.shape} -> {target_shape}")
        
        result = torch.zeros(target_shape, device=tensor.device, dtype=tensor.dtype)
        
        # Определяем, какие срезы копировать
        slices_src = []
        slices_dst = []
        
        for dim in range(min(len(tensor.shape), len(target_shape))):
            min_size = min(tensor.shape[dim], target_shape[dim])
            slices_src.append(slice(0, min_size))
            slices_dst.append(slice(0, min_size))
        
        # Дополняем до полной размерности
        while len(slices_src) < len(tensor.shape):
            slices_src.append(slice(None))
        while len(slices_dst) < len(target_shape):
            slices_dst.append(slice(None))
        
        # Копируем данные
        result[tuple(slices_dst)] = tensor[tuple(slices_src)]
        
        return result
    
    def _optimize_tensor_shape(self, shape: Tuple[int, ...]) -> Tuple[int, ...]:
        """Оптимизирует форму тензора по теории ТРАП."""
        if len(shape) >= 2:
            # Для матричных операций
            rows, cols = shape[-2], shape[-1]
            
            # Из экспериментов: оптимальные размеры 200, 400
            if rows <= 200:
                opt_rows = 200
            elif rows <= 400:
                opt_rows = 400
            else:
                opt_rows = self._find_nearest_resonant(rows)
            
            if cols <= 200:
                opt_cols = 200
            elif cols <= 400:
                opt_cols = 400
            else:
                opt_cols = self._find_nearest_resonant(cols)
            
            return shape[:-2] + (opt_rows, opt_cols)
        else:
            # Для векторов
            size = shape[0]
            if size <= 200:
                opt_size = 200
            elif size <= 400:
                opt_size = 400
            else:
                opt_size = self._find_nearest_resonant(size)
            return (opt_size,)
    
    def _find_nearest_resonant(self, size: int) -> int:
        """Находит ближайший резонансный размер."""
        if size <= 0:
            return 32
        
        distances = [(abs(size - rs), rs) for rs in self.resonant_sizes]
        distances.sort()
        return distances[0][1]
    
    def _get_gpu_energy(self) -> float:
        """Получает текущее энергопотребление GPU."""
        try:
            # Используем nvidia-smi через subprocess
            result = subprocess.run(
                ['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits'],
                capture_output=True, text=True, timeout=2
            )
            
            if result.returncode == 0 and result.stdout.strip():
                lines = result.stdout.strip().split('\n')
                if lines:
                    return float(lines[0].strip())
        except (subprocess.TimeoutExpired, ValueError, FileNotFoundError):
            pass
        
        # Возвращаем оценку на основе нагрузки
        if TORCH_AVAILABLE and torch.cuda.is_available():
            mem_allocated = torch.cuda.memory_allocated() / 1e9  # GB
            return mem_allocated * 50  # Примерная оценка: 50W на GB
        
        return 0.0
    
    def analyze_gpu_resonance(self, max_size: int = 2048, test_iterations: int = 10) -> Dict[str, Any]:
        """
        Анализ резонансных размеров для текущей GPU.
        
        Args:
            max_size: Максимальный размер для тестирования
            test_iterations: Количество итераций теста
            
        Returns:
            Результаты анализа
        """
        if not TORCH_AVAILABLE or not torch.cuda.is_available():
            return {"error": "GPU not available"}
        
        # Тестируем различные размеры
        test_sizes = []
        size = 32
        while size <= max_size:
            test_sizes.append(size)
            size = size * 2
        
        # Добавляем оптимальные размеры из экспериментов
        test_sizes.extend([25, 50, 100, 200, 400, 800])
        test_sizes = sorted(list(set([s for s in test_sizes if s <= max_size])))
        
        results = {}
        
        for size in test_sizes:
            try:
                # Создаем тестовые тензоры
                a = torch.randn(size, size, device=self.device, dtype=torch.float32)
                
                # Прогрев
                torch.matmul(a, a.t())
                torch.cuda.synchronize()
                
                # Замеряем производительность с нашим методом
                start_time = time.perf_counter()
                start_energy = self._get_gpu_energy()
                
                for _ in range(test_iterations):
                    c = self._ring_self_matmul(a)
                
                torch.cuda.synchronize()
                end_time = time.perf_counter()
                end_energy = self._get_gpu_energy()
                
                duration = end_time - start_time
                energy_used = end_energy - start_energy
                
                # Расчет метрик
                operations = 2 * size ** 3  # Умножение матриц: O(n^3)
                throughput = operations * test_iterations / duration / 1e9  # GFlops
                efficiency = throughput / energy_used if energy_used > 0 else 0
                
                # Измеряем память
                mem_allocated = torch.cuda.memory_allocated() / 1e9  # GB
                
                results[size] = {
                    'duration': duration,
                    'throughput_gflops': throughput,
                    'energy_used': energy_used,
                    'efficiency': efficiency,
                    'memory_gb': mem_allocated,
                    'operations': operations * test_iterations
                }
                
                # Очистка
                del a, c
                torch.cuda.empty_cache()
                
            except Exception as e:
                print(f"Error testing size {size}: {e}")
                continue
        
        # Анализ результатов
        if results:
            # Находим наиболее эффективные размеры
            sorted_by_efficiency = sorted(
                results.items(), 
                key=lambda x: x[1]['efficiency'], 
                reverse=True
            )
            
            resonant_sizes = [size for size, _ in sorted_by_efficiency[:3]]
            
            # Находим наиболее производительные размеры
            sorted_by_throughput = sorted(
                results.items(),
                key=lambda x: x[1]['throughput_gflops'],
                reverse=True
            )
            
            high_perf_sizes = [size for size, _ in sorted_by_throughput[:3]]
            
            return {
                'resonant_sizes': resonant_sizes,
                'high_performance_sizes': high_perf_sizes,
                'all_results': results,
                'optimal_size': 200,  # Из экспериментов ТРАП
                'recommended_sizes': [100, 200, 400, 800]
            }
        
        return {"error": "No results collected"}
    
    def test_accuracy(self, size: int = 100) -> Dict[str, Any]:
        """
        Тестирует точность кольцевого умножения.
        
        Args:
            size: Размер тестовой матрицы
            
        Returns:
            Результаты сравнения точности
        """
        if not TORCH_AVAILABLE:
            return {"error": "PyTorch not available"}
        
        # Создаем тестовую матрицу
        a = torch.randn(size, size, device=self.device)
        
        # Стандартное умножение
        correct = torch.matmul(a, a.t())
        
        # Наше кольцевое умножение
        ours = self._ring_self_matmul(a)
        
        # Вычисляем ошибку
        mse = torch.mean((correct - ours) ** 2).item()
        max_error = torch.max(torch.abs(correct - ours)).item()
        mean_error = torch.mean(torch.abs(correct - ours)).item()
        
        # Проверяем размеры
        size_match = correct.shape == ours.shape
        
        return {
            'size_match': size_match,
            'correct_shape': correct.shape,
            'our_shape': ours.shape,
            'mse': mse,
            'max_error': max_error,
            'mean_error': mean_error,
            'relative_error': mean_error / torch.mean(torch.abs(correct)).item() if torch.mean(torch.abs(correct)).item() > 0 else 0
        }


def test_optimizer():
    """Тестируем оптимизатор"""
    if not TORCH_AVAILABLE:
        print("PyTorch не установлен")
        return
    
    optimizer = GPURingOptimizer(device="cuda:0" if torch.cuda.is_available() else "cpu")
    
    # Тест 1: Проверка точности
    print("=" * 70)
    print("ТЕСТ ТОЧНОСТИ")
    print("=" * 70)
    
    for size in [5, 10, 50, 100, 200]:
        accuracy = optimizer.test_accuracy(size)
        print(f"\nРазмер {size}x{size}:")
        print(f"  Совпадение размеров: {'✓' if accuracy['size_match'] else '✗'}")
        print(f"  MSE ошибка: {accuracy['mse']:.6f}")
        print(f"  Максимальная ошибка: {accuracy['max_error']:.6f}")
        print(f"  Средняя ошибка: {accuracy['mean_error']:.6f}")
        print(f"  Относительная ошибка: {accuracy['relative_error']:.6%}")
    
    # Тест 2: Проверка разных операций
    print("\n" + "=" * 70)
    print("ТЕСТ ОПЕРАЦИЙ")
    print("=" * 70)
    
    test_sizes = [5, 10, 13, 20, 25, 50, 100, 513]
    
    print(f"{'Исходный размер':<15} {'Результирующий размер':<20} {'Совпадение':<10}")
    print("-" * 60)
    
    for size in test_sizes:
        a = torch.randn(size, size, device=optimizer.device if torch.cuda.is_available() else "cpu")
        
        # Смотрим что делает оптимизатор
        result = optimizer.optimize_tensor_operation(a, operation="matmul")
        
        match = "✓" if a.shape == result.shape else f"{size}→{result.shape[0]}"
        print(f"{size:>5}x{size:<9} {result.shape[0]:>5}x{result.shape[1]:<14} {match:>10}")
    
    # Тест 3: Производительность
    print("\n" + "=" * 70)
    print("ТЕСТ ПРОИЗВОДИТЕЛЬНОСТИ")
    print("=" * 70)
    
    if torch.cuda.is_available():
        size = 512
        a = torch.randn(size, size, device="cuda:0")
        
        # Стандартное умножение
        torch.cuda.synchronize()
        start = time.time()
        for _ in range(10):
            correct = torch.matmul(a, a.t())
        torch.cuda.synchronize()
        std_time = time.time() - start
        
        # Наше умножение
        torch.cuda.synchronize()
        start = time.time()
        for _ in range(10):
            ours = optimizer.optimize_tensor_operation(a, operation="matmul")
        torch.cuda.synchronize()
        our_time = time.time() - start
        
        # Проверка точности
        mse = torch.mean((correct - ours) ** 2).item()
        
        print(f"Стандартное умножение: {std_time:.4f} сек")
        print(f"Кольцевое умножение:  {our_time:.4f} сек")
        print(f"Ускорение: {std_time/our_time:.2f}x")
        print(f"MSE ошибка: {mse:.6f}")
        
        # Визуальное сравнение (первые 3x3)
        print("\nВизуальное сравнение (первые 3x3):")
        print("Стандартное:")
        print(correct[:3, :3].cpu().numpy())
        print("\nКольцевое:")
        print(ours[:3, :3].cpu().numpy())
        
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