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
                             workload_type: str = "normal",
                             iterations: int = 100) -> torch.Tensor:
        """
        Реальная реализация Ring Theory как в C#.

        Args:
            iterations: Количество итераций уравнения (аналог времени в C#)
        """
        if not TORCH_AVAILABLE:
            return tensor if tensor2 is None else tensor2

        if operation == "ring_field":  # НОВАЯ ОПЕРАЦИЯ!
            return self._simulate_ring_field(tensor, iterations, workload_type)
        elif operation == "matmul":
            # Для matmul оставляем старую логику
            return self._optimized_matmul_with_blocks(tensor, tensor2, workload_type)
        else:
            return tensor if tensor2 is None else tensor2

    def _simulate_ring_field(self, tensor: torch.Tensor,
                            iterations: int,
                            workload_type: str) -> torch.Tensor:
        """
        Симуляция кольцевого поля как в C# RingLoad.

        Вход: tensor shape [batch, channels, height, width] или [height, width]
        Возвращает: эволюционировавшее поле после iterations итераций
        """
        if len(tensor.shape) == 2:
            # Добавляем batch и channel размерности
            field = tensor.unsqueeze(0).unsqueeze(0)  # [1, 1, H, W]
        elif len(tensor.shape) == 4:
            field = tensor
        else:
            return tensor

        # Настройки в зависимости от нагрузки
        if workload_type == "heavy":
            dt = 0.05  # Меньший шаг для стабильности
            omega = 0.01  # Частота внешнего воздействия
        elif workload_type == "sequential":
            dt = 0.1
            omega = 0.02
        else:
            dt = 0.2
            omega = 0.03

        # Инициализируем 3 уровня как в C#
        # level0 - основное поле, level1 - вспомогательное, level2 - буфер
        levels = torch.zeros((3, field.shape[2], field.shape[3]), 
                            device=tensor.device, dtype=tensor.dtype)
        levels[0] = field[0, 0].clone()
        levels[1] = torch.tanh(levels[0])  # Начальное условие как в C#

        scale_factor = 1.0 / math.sqrt(field.shape[2])

        for iter in range(iterations):
            # Вычисляем лапласиан для каждого пикселя (как в C#)
            # Лапласиан = ∇²f = f(x-1,y) + f(x+1,y) + f(x,y-1) + f(x,y+1) - 4f(x,y)

            # Используем свертку для эффективного вычисления лапласиана
            laplacian_kernel = torch.tensor([
                [0, 1, 0],
                [1, -4, 1],
                [0, 1, 0]
            ], device=tensor.device, dtype=tensor.dtype).view(1, 1, 3, 3)

            # Вычисляем лапласиан для уровня 0
            laplacian = F.conv2d(levels[0].unsqueeze(0).unsqueeze(0),
                                laplacian_kernel,
                                padding=1).squeeze()

            # Уравнение синус-Гордона с внешней частотой (КАК В C#!)
            # dφ/dt = ∇²φ - sin(φ) + ε*sin(ωt)
            levels[0] += scale_factor * dt * (
                laplacian -
                torch.sin(levels[0]) +
                0.1 * torch.sin(iter * omega * scale_factor)
            )

            # Взаимодействие между уровнями (КАК В C#!)
            # level1 = 0.8*level1 + 0.2*tanh(level0)
            levels[1] = 0.8 * levels[1] + 0.2 * torch.tanh(levels[0])

            # Периодический обмен энергией между уровнями
            if iter % 50 == 0:
                # Сохраняем часть энергии в level2
                levels[2] = 0.5 * levels[0] + 0.5 * levels[2]
                # Возвращаем часть обратно
                levels[0] = 0.9 * levels[0] + 0.1 * levels[2]

        # Возвращаем результат в исходной форме
        result = levels[0].unsqueeze(0).unsqueeze(0)
        if len(tensor.shape) == 2:
            return result.squeeze()
        return result

    def _optimized_matmul_with_blocks(self, a: torch.Tensor, b: Optional[torch.Tensor],
                                     workload_type: str) -> torch.Tensor:
        """
        Оптимизированное умножение матриц с блочным разбиением.
        """
        if b is None:
            # Self-matmul: A * Aᵀ
            b = a.T

        # Определяем стратегию в зависимости от типа нагрузки
        if workload_type == "heavy":
            block_size = self._get_optimal_block_size_for_heavy_load(a.device)
            use_double_buffering = True
        elif workload_type == "sequential":
            block_size = self._get_cache_friendly_block_size(a.device)
            use_double_buffering = True
        elif workload_type == "light":
            # Для легкой нагрузки используем стандартное умножение
            return torch.matmul(a, b)
        else:
            block_size = self._get_optimal_block_size(a.device)
            use_double_buffering = False

        # Проверяем, нужно ли вообще использовать блочное умножение
        if self._should_use_blocked_matmul(a, b, block_size):
            return self._blocked_matmul(a, b, block_size, use_double_buffering)
        else:
            return torch.matmul(a, b)

    def _blocked_matmul(self, a: torch.Tensor, b: torch.Tensor,
                       block_size: int, use_double_buffering: bool) -> torch.Tensor:
        """
        Реализация блочного умножения матриц для оптимизации кэша.
        """
        m, k = a.shape[-2], a.shape[-1]
        k2, n = b.shape[-2], b.shape[-1]

        # Инициализируем результат
        result = torch.zeros((m, n), device=a.device, dtype=a.dtype)

        if use_double_buffering:
            # Используем двойную буферизацию для перекрытия вычислений и доступа к памяти
            return self._blocked_matmul_with_double_buffering(a, b, block_size)

        # Простое блочное умножение
        for i in range(0, m, block_size):
            i_end = min(i + block_size, m)
            for j in range(0, n, block_size):
                j_end = min(j + block_size, n)
                # Инициализируем аккумулятор для блока результата
                block_acc = torch.zeros((i_end - i, j_end - j),
                                        device=a.device,
                                        dtype=a.dtype)

                for l in range(0, k, block_size):
                    l_end = min(l + block_size, k)

                    # Берем блоки матриц
                    a_block = a[i:i_end, l:l_end]
                    b_block = b[l:l_end, j:j_end]

                    # Умножаем блоки и добавляем к аккумулятору
                    block_acc += torch.matmul(a_block, b_block)

                    # Принудительная синхронизация для лучшей предсказуемости
                    if l % (block_size * 4) == 0:
                        torch.cuda.synchronize()

                # Сохраняем результат блока
                result[i:i_end, j:j_end] = block_acc

        return result

    def _blocked_matmul_with_double_buffering(self, a: torch.Tensor, b: torch.Tensor,
                                             block_size: int) -> torch.Tensor:
        """
        Блочное умножение с двойной буферизацией для тяжелых нагрузок.
        """
        m, k = a.shape[-2], a.shape[-1]
        k2, n = b.shape[-2], b.shape[-1]

        result = torch.zeros((m, n), device=a.device, dtype=a.dtype)

        # Определяем количество потоков для асинхронных операций
        num_streams = min(4, torch.cuda.device_count())
        streams = [torch.cuda.Stream(device=a.device) for _ in range(num_streams)]

        # Разбиваем работу на части для разных потоков
        i_blocks = list(range(0, m, block_size))
        j_blocks = list(range(0, n, block_size))

        # Распределяем блоки по потокам
        from itertools import cycle
        stream_cycle = cycle(streams)

        # Создаем задачи для каждого блока
        tasks = []
        for i in i_blocks:
            i_end = min(i + block_size, m)
            for j in j_blocks:
                j_end = min(j + block_size, n)
                stream = next(stream_cycle)

                # Запускаем вычисление блока в отдельном потоке
                with torch.cuda.stream(stream):
                    block_acc = torch.zeros((i_end - i, j_end - j),
                                            device=a.device,
                                            dtype=a.dtype)

                    for l in range(0, k, block_size):
                        l_end = min(l + block_size, k)
                        a_block = a[i:i_end, l:l_end]
                        b_block = b[l:l_end, j:j_end]
                        block_acc += torch.matmul(a_block, b_block)

                    result[i:i_end, j:j_end] = block_acc

                tasks.append(stream)

        # Синхронизируем все потоки
        for stream in streams:
            stream.synchronize()

        return result

    def _get_optimal_block_size(self, device) -> int:
        """
        Определяет оптимальный размер блока для кэша конкретного GPU.
        """
        if not torch.cuda.is_available():
            return 256  # Значение по умолчанию для CPU

        props = torch.cuda.get_device_properties(device)

        # Архитектурно-зависимые настройки
        if props.major >= 8:  # Ampere и новее
            # Для тензорных ядер оптимальны размеры, кратные 32/64/128
            if props.total_memory <= 8e9:  # 8 GB
                return 512
            elif props.total_memory <= 16e9:  # 16 GB
                return 768
            else:
                return 1024
        elif props.major >= 7:  # Volta, Turing
            return 512
        elif props.major >= 6:  # Pascal
            return 256
        else:  # Более старые архитектуры
            return 128

    def _get_optimal_block_size_for_heavy_load(self, device) -> int:
        """
        Оптимальный размер блока для тяжелых нагрузок (последовательных операций).
        """
        base_size = self._get_optimal_block_size(device)

        # Для тяжелых нагрузок уменьшаем размер блока,
        # чтобы лучше помещаться в L1/L2 кэш
        if torch.cuda.is_available():
            props = torch.cuda.get_device_properties(device)

            # Оцениваем размер кэша L2 (примерно)
            # RTX 3090: 6MB, RTX 4090: 72MB и т.д.
            if props.major >= 8 and props.total_memory > 16e9:
                # Большие GPU с большим кэшем
                return min(base_size, 768)
            else:
                return min(base_size, 512)

        return min(base_size, 256)

    def _get_cache_friendly_block_size(self, device) -> int:
        """
        Размер блока, дружественный к кэшу для последовательных операций.
        """
        # Выбираем размеры, которые хорошо делят типичные размеры матриц
        cache_friendly_sizes = [64, 128, 256, 512, 768, 1024]

        if torch.cuda.is_available():
            props = torch.cuda.get_device_properties(device)

            # Для кэша L1 (обычно 64-128KB) и float32
            # Максимальный блок, который помещается в L1:
            # block_size * block_size * 4 байта ≤ размер_L1
            l1_size_kb = 64  # Консервативная оценка
            max_block_for_l1 = int(math.sqrt(l1_size_kb * 1024 / 4))

            suitable_sizes = [s for s in cache_friendly_sizes if s <= max_block_for_l1]
            if suitable_sizes:
                return max(suitable_sizes)

        return 256

    def _should_use_blocked_matmul(self, a: torch.Tensor, b: torch.Tensor,
                                  block_size: int) -> bool:
        """
        Определяет, стоит ли использовать блочное умножение.
        """
        m, k = a.shape[-2], a.shape[-1]
        n = b.shape[-1]

        # Для маленьких матриц блочное умножение неэффективно
        if m < 256 and n < 256 and k < 256:
            return False

        # Для очень больших матриц всегда используем блочное умножение
        if m > 2048 or n > 2048 or k > 2048:
            return True

        # Проверяем, являются ли размеры оптимальными для прямого умножения
        # (степени двойки часто уже хорошо оптимизированы в cuBLAS)
        def is_power_of_two_or_close(n):
            if n <= 0:
                return False
            # Проверяем степень двойки
            if (n & (n - 1)) == 0:
                return True
            # Или близко к степени двойки (в пределах 10%)
            closest_power = 2 ** int(math.log2(n))
            return abs(n - closest_power) / closest_power < 0.1

        # Если размеры уже оптимальны, используем прямое умножение
        if (is_power_of_two_or_close(m) and
            is_power_of_two_or_close(n) and
            is_power_of_two_or_close(k)):
            return False

        return True

    def _optimized_convolution(self, x: torch.Tensor, workload_type: str) -> torch.Tensor:
        """
        Оптимизированная свертка с учетом типа нагрузки.
        """
        if len(x.shape) == 4:  # [batch, channels, height, width]
            # Выбираем оптимальный размер ядра
            kernel_size = self._get_optimal_kernel_size(x.shape[-2:], workload_type)

            # Создаем ядро с оптимальными свойствами
            weight = self._create_optimal_kernel(x.shape[1], kernel_size, x.device)

            # Оптимизируем паддинг
            padding = self._get_optimal_padding(kernel_size, workload_type)

            return F.conv2d(x, weight, padding=padding)
        else:
            return x

    def _optimized_elementwise(self, a: torch.Tensor, b: torch.Tensor,
                              operation: str) -> torch.Tensor:
        """
        Оптимизированные поэлементные операции.
        """
        # Проверяем совместимость размеров
        if a.shape != b.shape:
            # Пытаемся broadcast
            try:
                if operation == "add":
                    return a + b
                elif operation == "mul":
                    return a * b
            except:
                pass
            return a  # fallback

        # Используем оптимальную стратегию для поэлементных операций
        if operation == "add":
            return self._optimized_add(a, b)
        elif operation == "mul":
            return self._optimized_mul(a, b)
        else:
            return a  # fallback

    def _optimized_add(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        """
        Оптимизированное сложение с учетом работы с памятью.
        """
        # Для больших тензоров используем in-place операции когда возможно
        if a.is_contiguous() and b.is_contiguous() and a.numel() > 1000000:
            result = a.clone()
            result.add_(b)
            return result
        else:
            return a + b

    def _optimized_mul(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        """
        Оптимизированное умножение с учетом работы с памятью.
        """
        if a.is_contiguous() and b.is_contiguous() and a.numel() > 1000000:
            result = a.clone()
            result.mul_(b)
            return result
        else:
            return a * b

    def _update_load_history(self, shape, operation, workload_type):
        """
        Обновляет историю нагрузок для анализа паттернов.
        """
        self.load_history.append({
            'timestamp': time.time(),
            'shape': shape,
            'operation': operation,
            'workload_type': workload_type
        })

        # Ограничиваем размер истории
        if len(self.load_history) > 1000:
            self.load_history = self.load_history[-1000:]

        # Анализируем паттерны для автоматической настройки
        if len(self.load_history) % 100 == 0:
            self._analyze_load_patterns()

    def _analyze_load_patterns(self):
        """
        Анализирует паттерны нагрузок для автоматической оптимизации.
        """
        if len(self.load_history) < 50:
            return

        # Анализируем частоту операций
        op_counts = {}
        for entry in self.load_history[-100:]:
            op = entry['operation']
            op_counts[op] = op_counts.get(op, 0) + 1

        # Анализируем типичные размеры
        sizes = []
        for entry in self.load_history[-100:]:
            if 'shape' in entry:
                sizes.append(entry['shape'])

        # Сохраняем статистику для использования в оптимизациях
        self.operation_stats = {
            'common_operations': op_counts,
            'typical_sizes': sizes[-10:] if sizes else [],
            'workload_distribution': {}
        }

        # Анализируем распределение типов нагрузки
        for entry in self.load_history[-100:]:
            wt = entry.get('workload_type', 'normal')
            self.operation_stats['workload_distribution'][wt] = \
                self.operation_stats['workload_distribution'].get(wt, 0) + 1

    def _get_optimal_kernel_size(self, input_size, workload_type):
        """
        Определяет оптимальный размер ядра свертки.
        """
        # Базовые эвристики
        if workload_type == "heavy":
            return 3  # Маленькое ядро для тяжелых нагрузок
        elif workload_type == "sequential":
            return 5  # Среднее ядро для последовательных операций
        else:
            # Выбираем на основе размера входа
            h, w = input_size
            if h * w < 64 * 64:
                return 3
            elif h * w < 256 * 256:
                return 5
            else:
                return 7

    def _create_optimal_kernel(self, channels, kernel_size, device):
        """
        Создает оптимальное ядро свертки.
        """
        # Используем ядро Гаусса для плавности
        import numpy as np
        kernel = np.fromfunction(
            lambda x, y: np.exp(-((x - kernel_size//2)**2 + (y - kernel_size//2)**2) / 
                              (2 * (kernel_size/4)**2)),
            (kernel_size, kernel_size)
        )
        kernel = kernel / kernel.sum()

        # Преобразуем в тензор PyTorch
        weight = torch.tensor(kernel, device=device, dtype=torch.float32)
        weight = weight.view(1, 1, kernel_size, kernel_size)

        # Масштабируем по каналам
        if channels > 1:
            weight = weight.repeat(channels, 1, 1, 1)

        return weight

    def _get_optimal_padding(self, kernel_size, workload_type):
        """
        Определяет оптимальный паддинг для свертки.
        """
        if workload_type == "sequential":
            return kernel_size // 2  # Стандартный паддинг для сохранения размера
        else:
            return max(0, kernel_size // 2 - 1)  # Чуть меньше паддинга для экономии памяти
    
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
        """
        Умножение матриц, вдохновленное кольцевой теорией.
        Использует блочное разбиение для оптимизации работы с кэшем.
        """
        # 1. Определяем оптимальный размер блока для данного GPU
        #    (вместо паддинга всего тензора)
        block_size = self._get_optimal_block_size(a.device)

        m, k = a.shape[-2], a.shape[-1]
        k2, n = b.shape[-2], b.shape[-1]

        # Инициализируем результат
        result = torch.zeros((m, n), device=a.device, dtype=a.dtype)

        # 2. Блочное умножение (как в алгоритме из кэша)
        #    Этот подход сам по себе энергоэффективен.
        for i in range(0, m, block_size):
            i_end = min(i + block_size, m)
            for j in range(0, n, block_size):
                j_end = min(j + block_size, n)
                # Аккумулируем результат для блока [i:i_end, j:j_end]
                block_result = torch.zeros((i_end - i, j_end - j),
                                            device=a.device,
                                            dtype=a.dtype)
                for l in range(0, k, block_size):
                    l_end = min(l + block_size, k)
                    # Берем блоки из A и B, которые уже могут быть в кэше
                    a_block = a[i:i_end, l:l_end]
                    b_block = b[l:l_end, j:j_end]
                    block_result += torch.matmul(a_block, b_block)
                result[i:i_end, j:j_end] = block_result

        return result
    
    def _get_optimal_block_size(self, device):
        """Определяет лучший размер блока для кэша конкретного GPU."""
        # Эмпирические значения для начала. Можно усложнить логику.
        props = torch.cuda.get_device_properties(device)
        # Ориентируемся на размер кэша L1/L2 (упрощенно)
        if props.total_memory <= 8e9:  # 8 GB
            return 256
        elif props.total_memory <= 16e9:  # 16 GB
            return 512
        else:  # Больше памяти, можно брать больше блок (но осторожно!)
            return 1024 if props.major >= 7 else 512  # Учитываем и архитектуру
    
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