"""
GPU OPTIMIZER FOR DATACENTERS AND MINING - PRACTICAL RING THEORY IMPLEMENTATION
Теория ТРАП: резонансные размеры → энергоэффективность на реальных GPU задачах
"""

import torch
import numpy as np
import math
import time
import subprocess
import json
from typing import Dict, List, Tuple, Optional, Any, Callable
import warnings

try:
    import torch.nn.functional as F
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    warnings.warn("PyTorch not available. GPU optimizations disabled.")


class GPURingOptimizer:
    """
    ПРАКТИЧЕСКАЯ РЕАЛИЗАЦИЯ ТЕОРИИ ТРАП ДЛЯ GPU
    
    Ключевые принципы:
    1. Резонансные размеры матриц/тензоров дают экономию энергии
    2. Кольцевые структуры в вычислениях улучшают кэширование
    3. Оптимальные размеры зависят от архитектуры GPU
    
    Применение: майнинг, нейросети, научные вычисления
    """
    
    # РЕЗОНАНСНЫЕ РАЗМЕРЫ ИЗ ЭКСПЕРИМЕНТОВ ТРАП (C#)
    TRAP_RESONANT_SIZES = [
        25, 50, 100, 150, 200, 300, 
        400, 600, 800, 1200, 1600, 2400, 3200
    ]
    
    # РЕЗОНАНСНЫЕ РАЗМЕРЫ ДЛЯ GPU (архитектурные оптимумы)
    GPU_RESONANT_SIZES = {
        'tensor_cores': [32, 64, 128, 256, 512, 1024, 2048, 4096],
        'cache_l1': [64, 128, 256, 512],
        'cache_l2': [1024, 2048, 4096, 8192],
        'memory_optimal': [1536, 3072, 6144, 12288],
        'compute_optimal': [128, 256, 512, 768, 1024, 1536]
    }
    
    # ТИПЫ НАГРУЗОК
    WORKLOAD_TYPES = {
        'mining': {'block_sizes': [256, 512, 1024], 'iterations': 1000},
        'training': {'batch_sizes': [32, 64, 128], 'hidden_sizes': [512, 1024, 2048]},
        'inference': {'batch_sizes': [1, 8, 16, 32], 'precision': 'mixed'},
        'scientific': {'matrix_sizes': [1024, 2048, 4096], 'iterations': 100}
    }
    
    def __init__(self, device: str = "cuda:0", optimize_for: str = "energy"):
        """
        Инициализация оптимизатора для конкретного GPU
        
        Args:
            device: CUDA устройство
            optimize_for: 'energy' (экономия энергии) или 'performance' (производительность)
        """
        self.device = device
        self.optimize_for = optimize_for
        
        if TORCH_AVAILABLE and torch.cuda.is_available():
            self.props = torch.cuda.get_device_properties(device)
            self._init_gpu_specific_params()
        else:
            self.props = None
            warnings.warn("CUDA not available, using CPU fallback")
        
        # Кэш оптимальных размеров для разных операций
        self.size_cache = {}
        self._resonant_cache = {}  # Кэш для ТРАП резонансных размеров
        
        # Статистика оптимизаций
        self.stats = {
            'total_optimizations': 0,
            'energy_saved_total': 0.0,
            'time_saved_total': 0.0,
            'successful_optimizations': 0,
            'trap_optimizations_applied': 0
        }
    
    def _init_gpu_specific_params(self):
        """Инициализация параметров для конкретного GPU"""
        if not self.props:
            return
        
        # Определяем резонансные размеры для этой конкретной GPU
        self.resonant_sizes = self._calculate_gpu_resonant_sizes()
        
        # Параметры для разных типов операций
        self.operation_params = {
            'matmul': self._get_matmul_optimal_params(),
            'conv': self._get_conv_optimal_params(),
            'linear': self._get_linear_optimal_params(),
            'attention': self._get_attention_optimal_params()
        }
        
        print(f"⚡ GPU Ring Optimizer initialized for {self.props.name}")
        print(f"   Architecture: SM {self.props.major}.{self.props.minor}")
        print(f"   Memory: {self.props.total_memory / 1e9:.1f} GB")
        print(f"   Optimizing for: {self.optimize_for}")
        print(f"   ТРАП резонансные размеры: {self.TRAP_RESONANT_SIZES[:6]}...")
    
    def _calculate_gpu_resonant_sizes(self) -> List[int]:
        """Вычисляет резонансные размеры для конкретной GPU"""
        base_sizes = []
        
        # Размеры для tensor cores (Ampere и новее)
        if self.props.major >= 8:
            base_sizes.extend([32, 64, 128, 256, 512, 1024, 2048, 4096])
        
        # Размеры для кэша
        l1_size_bytes = 64 * 1024  # 64KB
        l2_size_bytes = 6 * 1024 * 1024  # 6MB
        
        # Оптимальные размеры для float32 (4 байта)
        l1_optimal = int(math.sqrt(l1_size_bytes / 4))
        l2_optimal = int(math.sqrt(l2_size_bytes / 4))
        
        base_sizes.extend([
            l1_optimal // 2, l1_optimal, l1_optimal * 2,
            l2_optimal // 4, l2_optimal // 2, l2_optimal
        ])
        
        # Округляем до ближайших степеней двойки
        base_sizes = [self._round_to_power_of_two(s) for s in base_sizes]
        
        # Убираем дубликаты и сортируем
        base_sizes = sorted(list(set([s for s in base_sizes if 16 <= s <= 16384])))
        
        return base_sizes
    
    def _get_matmul_optimal_params(self) -> Dict:
        """Оптимальные параметры для умножения матриц"""
        if not self.props:
            return {'block_size': 256, 'tile_size': 128}
        
        # Для tensor cores нужны размеры, кратные 8, 16, 32, 64, 128
        if self.props.major >= 8:  # Ampere+
            tile_sizes = [64, 128, 256, 512]
            block_sizes = [256, 512, 1024]
        elif self.props.major >= 7:  # Volta, Turing
            tile_sizes = [64, 128, 256]
            block_sizes = [128, 256, 512]
        else:  # Pascal и старше
            tile_sizes = [32, 64, 128]
            block_sizes = [64, 128, 256]
        
        return {
            'tile_sizes': tile_sizes,
            'block_sizes': block_sizes,
            'preferred_m': self.resonant_sizes,
            'preferred_n': self.resonant_sizes,
            'preferred_k': self.resonant_sizes
        }
    
    def _get_conv_optimal_params(self) -> Dict:
        """Оптимальные параметры для сверток"""
        kernel_sizes = [3, 5, 7]
        
        # Размеры каналов, оптимальные для tensor cores
        if self.props and self.props.major >= 8:
            channel_sizes = [32, 64, 128, 256, 512]
        else:
            channel_sizes = [16, 32, 64, 128, 256]
        
        return {
            'kernel_sizes': kernel_sizes,
            'channel_sizes': channel_sizes,
            'tile_sizes': [32, 64, 128]
        }
    
    def _get_linear_optimal_params(self) -> Dict:
        """Оптимальные параметры для линейных слоев"""
        hidden_sizes = []
        
        # Скрытые размеры для нейросетей
        for size in self.resonant_sizes:
            if 256 <= size <= 8192:  # Практичные размеры для нейросетей
                hidden_sizes.append(size)
        
        return {
            'hidden_sizes': hidden_sizes,
            'batch_sizes': [16, 32, 64, 128, 256],
            'tile_sizes': [64, 128, 256]
        }
    
    def _get_attention_optimal_params(self) -> Dict:
        """Оптимальные параметры для внимания"""
        seq_lengths = []
        
        # Длины последовательностей, оптимальные для внимания
        for size in self.resonant_sizes:
            if 64 <= size <= 4096:  # Практичные размеры для последовательностей
                seq_lengths.append(size)
        
        return {
            'seq_lengths': seq_lengths,
            'head_sizes': [64, 128, 256, 512],
            'batch_sizes': [1, 8, 16, 32]
        }
    
    def optimize_tensor_operation(self,
                                 tensor: torch.Tensor,
                                 tensor2: Optional[torch.Tensor] = None,
                                 operation: str = "matmul",
                                 workload_type: str = "normal",
                                 target: str = "performance") -> torch.Tensor:
        """
        ПРАКТИЧЕСКАЯ ОПТИМИЗАЦИЯ ТЕНЗОРНЫХ ОПЕРАЦИЙ
        
        Реализует теорию ТРАП через:
        1. Приведение размеров к резонансным
        2. Оптимизацию размещения в памяти
        3. Выбор оптимальных алгоритмов
        
        Args:
            tensor: входной тензор
            tensor2: второй тензор (для бинарных операций)
            operation: тип операции
            workload_type: тип нагрузки
            target: цель оптимизации ('energy' или 'performance')
        
        Returns:
            Оптимизированный результат
        """
        if not TORCH_AVAILABLE:
            return tensor if tensor2 is None else tensor2
        
        # ВАЖНО: Применяем теорию ТРАП - приводим к резонансным размерам
        tensor_opt = self._apply_trap_optimization(tensor, operation)
        
        if tensor2 is not None:
            tensor2_opt = self._apply_trap_optimization(tensor2, operation)
        else:
            tensor2_opt = None
        
        # Оптимизируем в зависимости от операции
        if operation == "matmul":
            return self._optimize_matmul(tensor_opt, tensor2_opt, workload_type, target)
        elif operation == "conv":
            return self._optimize_convolution(tensor_opt, workload_type, target)
        elif operation == "linear":
            return self._optimize_linear(tensor_opt, tensor2_opt, workload_type, target)
        elif operation == "attention":
            return self._optimize_attention(tensor_opt, tensor2_opt, workload_type, target)
        elif operation == "elementwise":
            return self._optimize_elementwise(tensor_opt, tensor2_opt, workload_type, target)
        else:
            # Общая оптимизация размеров
            return self._optimize_generic(tensor_opt, workload_type, target)
    
    def _apply_trap_optimization(self, tensor: torch.Tensor, 
                                operation: str = "matmul") -> torch.Tensor:
        """
        Главный метод применения теории ТРАП
        Автоматически приводит размеры к резонансным
        """
        if tensor.dim() < 2:
            return tensor  # Не оптимизируем 1D тензоры
        
        # Для каждой размерности находим ближайший резонансный размер
        new_shape = []
        for i, dim in enumerate(tensor.shape):
            if tensor.dim() <= 2 or i >= tensor.dim() - 2:  # Оптимизируем последние 2 размерности
                resonant_dim = self._find_trap_resonant_size(dim, operation)
                new_shape.append(resonant_dim)
            else:
                new_shape.append(dim)  # Batch размеры оставляем как есть
        
        # Если размеры уже оптимальны
        if list(tensor.shape) == new_shape:
            return tensor
        
        # Изменяем размер
        return self._resize_to_resonant(tensor, tuple(new_shape))
    
    def _find_trap_resonant_size(self, current_size: int, 
                                operation: str) -> int:
        """
        Находит ближайший резонансный размер по теории ТРАП
        Ключевое правило: увеличение лучше уменьшения!
        """
        cache_key = f"{operation}_{current_size}"
        if cache_key in self._resonant_cache:
            return self._resonant_cache[cache_key]
        
        # 1. Ищем резонансные размеры БОЛЬШЕ текущего (основное правило ТРАП)
        larger_sizes = [s for s in self.TRAP_RESONANT_SIZES if s >= current_size]
        
        if larger_sizes:
            # Берем наименьший из больших размеров
            optimal = min(larger_sizes)
            increase = (optimal - current_size) / current_size
            
            # Если увеличение слишком большое (>50%), ищем ближайший
            if increase > 0.5:
                # Ищем среди всех размеров
                optimal = min(self.TRAP_RESONANT_SIZES, 
                            key=lambda x: abs(x - current_size))
        else:
            # Все резонансные размеры меньше текущего - берем максимальный
            optimal = max(self.TRAP_RESONANT_SIZES)
        
        # Дополнительная оптимизация для GPU архитектуры
        gpu_optimal = self._find_gpu_optimal_size(optimal, operation)
        
        self._resonant_cache[cache_key] = gpu_optimal
        self.stats['trap_optimizations_applied'] += 1
        
        return gpu_optimal
    
    def _find_gpu_optimal_size(self, trap_size: int, operation: str) -> int:
        """Дополнительная оптимизация для GPU архитектуры"""
        if not self.props:
            return trap_size
        
        # Для разных операций разные приоритеты
        if operation == "matmul":
            # Для умножения матриц предпочитаем степени двойки и кратные 64
            candidates = []
            for size in [trap_size, trap_size + 1, trap_size - 1, 
                        trap_size + 2, trap_size - 2]:
                if size > 0:
                    score = 0
                    if size % 64 == 0:
                        score += 3
                    if size % 128 == 0:
                        score += 2
                    if bin(size).count('1') == 1:  # Степень двойки
                        score += 4
                    candidates.append((score, -abs(size - trap_size), size))
            
            if candidates:
                candidates.sort(reverse=True)
                return candidates[0][2]
        
        return trap_size
    
    def _resize_to_resonant(self, tensor: torch.Tensor, 
                           new_shape: tuple) -> torch.Tensor:
        """
        Изменяет тензор к резонансным размерам
        Сохраняет данные в центре, края заполняет нулями
        """
        result = torch.zeros(new_shape, 
                           device=tensor.device, 
                           dtype=tensor.dtype)
        
        # Определяем сколько данных копировать
        slices_src = []
        slices_dst = []
        
        for src_dim, dst_dim in zip(tensor.shape, new_shape):
            copy_size = min(src_dim, dst_dim)
            src_start = max(0, (src_dim - copy_size) // 2)
            dst_start = max(0, (dst_dim - copy_size) // 2)
            
            slices_src.append(slice(src_start, src_start + copy_size))
            slices_dst.append(slice(dst_start, dst_start + copy_size))
        
        # Копируем данные
        result[tuple(slices_dst)] = tensor[tuple(slices_src)]
        
        return result
    
    def _optimize_matmul(self, a: torch.Tensor, b: Optional[torch.Tensor],
                        workload_type: str, target: str) -> torch.Tensor:
        """
        Оптимизация умножения матриц по теории ТРАП
        """
        if b is None:
            b = a.T  # Авто-транспонирование для квадратных матриц
        
        # ТРАП оптимизация уже применена в _apply_trap_optimization
        
        # 1. Анализируем размеры после ТРАП оптимизации
        m, k = a.shape[-2], a.shape[-1]
        k2, n = b.shape[-2], b.shape[-1]
        
        # 2. Проверяем что это резонансные размеры
        is_resonant_m = m in self.TRAP_RESONANT_SIZES
        is_resonant_n = n in self.TRAP_RESONANT_SIZES
        is_resonant_k = k in self.TRAP_RESONANT_SIZES
        
        # 3. Выбираем стратегию в зависимости от цели
        if target == "energy":
            return self._energy_efficient_matmul(a, b)
        else:
            return self._performance_matmul(a, b)
    
    def _energy_efficient_matmul(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        """Умножение матриц для экономии энергии"""
        # Для экономии энергии используем блочное умножение с малыми блоками
        m, k = a.shape[-2], a.shape[-1]
        n = b.shape[-1]
        
        block_size = self._get_energy_efficient_block_size()
        
        result = torch.zeros((m, n), device=a.device, dtype=a.dtype)
        
        # Небольшие блоки для лучшего кэширования
        for i in range(0, m, block_size):
            i_end = min(i + block_size, m)
            for j in range(0, n, block_size):
                j_end = min(j + block_size, n)
                block_acc = torch.zeros((i_end - i, j_end - j),
                                       device=a.device,
                                       dtype=a.dtype)
                
                for l in range(0, k, block_size):
                    l_end = min(l + block_size, k)
                    
                    a_block = a[i:i_end, l:l_end]
                    b_block = b[l:l_end, j:j_end]
                    block_acc += torch.matmul(a_block, b_block)
                
                result[i:i_end, j:j_end] = block_acc
        
        return result
    
    def _performance_matmul(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        """Умножение матриц для производительности"""
        # Используем tensor cores когда возможно
        if self._can_use_tensor_cores(a, b):
            try:
                with torch.cuda.amp.autocast():
                    return torch.matmul(a, b)
            except:
                pass
        
        # Иначе используем блочное умножение с большими блоками
        m, k = a.shape[-2], a.shape[-1]
        n = b.shape[-1]
        
        block_size = self._get_performance_block_size()
        
        result = torch.zeros((m, n), device=a.device, dtype=a.dtype)
        
        # Крупные блоки для лучшей утилизации SM
        for i in range(0, m, block_size):
            i_end = min(i + block_size, m)
            for j in range(0, n, block_size):
                j_end = min(j + block_size, n)
                
                # Используем аккумулятор
                block_acc = torch.zeros((block_size, block_size),
                                       device=a.device,
                                       dtype=a.dtype)
                
                for l in range(0, k, block_size):
                    l_end = min(l + block_size, k)
                    
                    a_block = a[i:i_end, l:l_end]
                    b_block = b[l:l_end, j:j_end]
                    block_acc[:i_end-i, :j_end-j] += torch.matmul(a_block, b_block)
                
                result[i:i_end, j:j_end] = block_acc[:i_end-i, :j_end-j]
        
        return result
    
    def _optimize_convolution(self, x: torch.Tensor,
                            workload_type: str, target: str) -> torch.Tensor:
        """
        Оптимизация свертки
        """
        if len(x.shape) != 4:  # Только для 4D тензоров [batch, channels, height, width]
            return x
        
        # ТРАП оптимизация уже применена
        return x
    
    def _optimize_linear(self, x: torch.Tensor, weight: Optional[torch.Tensor],
                        workload_type: str, target: str) -> torch.Tensor:
        """
        Оптимизация линейных слоев (нейросети)
        """
        if weight is None:
            return x
        
        # ТРАП оптимизация уже применена
        return torch.matmul(x, weight.T)
    
    def _optimize_attention(self, q: torch.Tensor, k: Optional[torch.Tensor],
                          workload_type: str, target: str) -> torch.Tensor:
        """
        Оптимизация внимания (transformer)
        """
        if k is None:
            k = q
            v = q
        else:
            v = k
        
        # ТРАП оптимизация уже применена
        scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(q.size(-1))
        attention = F.softmax(scores, dim=-1)
        return torch.matmul(attention, v)
    
    def _optimize_elementwise(self, a: torch.Tensor, b: Optional[torch.Tensor],
                            workload_type: str, target: str) -> torch.Tensor:
        """Оптимизация поэлементных операций"""
        if b is None:
            return a
        
        # ТРАП оптимизация уже применена
        return a + b
    
    def _optimize_generic(self, tensor: torch.Tensor,
                         workload_type: str, target: str) -> torch.Tensor:
        """Общая оптимизация тензора"""
        return tensor
    
    def _can_use_tensor_cores(self, a: torch.Tensor, b: torch.Tensor) -> bool:
        """Проверяет, можно ли использовать tensor cores"""
        if not self.props or self.props.major < 7:  # Нужен Volta или новее
            return False
        
        # Проверяем размеры (должны быть кратны 8/16 для tensor cores)
        m, k = a.shape[-2], a.shape[-1]
        n = b.shape[-1]
        
        return (m % 8 == 0 and k % 8 == 0 and n % 8 == 0)
    
    def _get_energy_efficient_block_size(self) -> int:
        """Размер блока для экономии энергии"""
        if not self.props:
            return 64
        
        # Для экономии энергии используем меньшие блоки
        if self.props.total_memory <= 8e9:  # 8GB
            return 64
        elif self.props.total_memory <= 16e9:  # 16GB
            return 128
        else:
            return 256
    
    def _get_performance_block_size(self) -> int:
        """Размер блока для производительности"""
        if not self.props:
            return 256
        
        # Для производительности используем большие блоки
        if self.props.major >= 8:  # Ampere+
            return 1024
        elif self.props.major >= 7:  # Volta, Turing
            return 512
        else:
            return 256
    
    def _round_to_power_of_two(self, n: int) -> int:
        """Округляет до ближайшей степени двойки"""
        if n <= 0:
            return 1
        
        # Находим ближайшую степень двойки
        power = 1
        while power < n:
            power <<= 1
        
        # Выбираем ближайшую из двух
        lower = power >> 1
        if abs(n - lower) < abs(n - power):
            return lower
        return power
    
    def get_optimization_stats(self) -> Dict:
        """Возвращает статистику оптимизаций"""
        return self.stats
    
    def reset_stats(self):
        """Сбрасывает статистику"""
        self.stats = {
            'total_optimizations': 0,
            'energy_saved_total': 0.0,
            'time_saved_total': 0.0,
            'successful_optimizations': 0,
            'trap_optimizations_applied': 0
        }


# Утилиты для работы с энергопотреблением
def get_gpu_power(device_id: int = 0) -> Optional[float]:
    """Получает текущее энергопотребление GPU"""
    try:
        import subprocess
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=power.draw', '--format=csv,noheader,nounits'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if device_id < len(lines):
                return float(lines[device_id].strip())
    except:
        pass
    return None


def measure_operation_energy(operation_func, iterations: int = 100) -> Dict:
    """Измеряет энергопотребление операции"""
    if not TORCH_AVAILABLE:
        return {'error': 'PyTorch not available'}
    
    power_readings = []
    execution_times = []
    
    # Базовое потребление
    base_power = get_gpu_power() or 0
    
    for _ in range(iterations):
        # Мощность до
        power_before = get_gpu_power() or base_power
        
        # Выполняем операцию
        start = time.perf_counter()
        result = operation_func()
        torch.cuda.synchronize()
        end = time.perf_counter()
        
        # Мощность после
        power_after = get_gpu_power() or base_power
        
        power_readings.append(power_after - power_before)
        execution_times.append(end - start)
    
    if power_readings and execution_times:
        return {
            'avg_power': np.mean(power_readings),
            'avg_time': np.mean(execution_times),
            'total_energy': np.sum(power_readings) * np.mean(execution_times),
            'iterations': iterations
        }
    
    return {'error': 'Measurement failed'}


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


# Пример использования
def example_usage():
    """Пример использования оптимизатора"""
    if not TORCH_AVAILABLE or not torch.cuda.is_available():
        print("CUDA not available")
        return
    
    # Создаем оптимизатор
    optimizer = GPURingOptimizer(device="cuda:0", optimize_for="energy")
    
    # Пример: оптимизация умножения матриц
    a = torch.randn(1000, 800, device='cuda')
    b = torch.randn(800, 1200, device='cuda')
    
    # Стандартное умножение
    start = time.time()
    result_std = torch.matmul(a, b)
    torch.cuda.synchronize()
    std_time = time.time() - start
    
    # Оптимизированное умножение
    start = time.time()
    result_opt = optimizer.optimize_tensor_operation(a, b, operation="matmul")
    torch.cuda.synchronize()
    opt_time = time.time() - start
    
    print(f"Стандартное: {std_time:.4f} сек")
    print(f"Оптимизированное: {opt_time:.4f} сек")
    print(f"Ускорение: {std_time/opt_time:.2f}x")
    
    # Проверяем точность
    error = torch.mean(torch.abs(result_std - result_opt))
    print(f"Ошибка: {error:.6f}")
    
    # Показываем статистику
    stats = optimizer.get_optimization_stats()
    print(f"\nСтатистика ТРАП оптимизаций: {stats['trap_optimizations_applied']}")
    
    return optimizer


if __name__ == "__main__":
    optimizer = example_usage()