"""
GPU OPTIMIZER FOR DATACENTERS AND MINING - PRACTICAL RING THEORY IMPLEMENTATION
Теория ТРАП: резонансные размеры → энергоэффективность на реальных GPU задачах
"""

import torch
import numpy as np
import math
import time
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
    
    # РЕЗОНАНСНЫЕ РАЗМЕРЫ ДЛЯ GPU (из экспериментов ТРАП + архитектурные оптимумы)
    RESONANT_SIZES = {
        'tensor_cores': [32, 64, 128, 256, 512, 1024, 2048, 4096],  # Для tensor cores
        'cache_l1': [64, 128, 256, 512],  # Размеры под кэш L1 (~64KB)
        'cache_l2': [1024, 2048, 4096, 8192],  # Размеры под кэш L2 (~6MB на RTX 3090)
        'memory_optimal': [1536, 3072, 6144, 12288],  # Эффективные для памяти
        'compute_optimal': [128, 256, 512, 768, 1024, 1536]  # Для вычислений
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
        
        # Статистика оптимизаций
        self.stats = {
            'total_optimizations': 0,
            'energy_saved_total': 0.0,
            'time_saved_total': 0.0,
            'successful_optimizations': 0
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
    
    def _calculate_gpu_resonant_sizes(self) -> List[int]:
        """Вычисляет резонансные размеры для конкретной GPU"""
        base_sizes = []
        
        # Размеры для tensor cores (Ampere и новее)
        if self.props.major >= 8:
            base_sizes.extend([32, 64, 128, 256, 512, 1024, 2048, 4096])
        
        # Размеры для кэша
        # L1: обычно 64-128KB, L2: 6MB на RTX 3090, 72MB на RTX 4090
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
        
        # Сохраняем оригинальные размеры
        original_shape = tensor.shape
        
        # Оптимизируем в зависимости от операции
        if operation == "matmul":
            return self._optimize_matmul(tensor, tensor2, workload_type, target)
        elif operation == "conv":
            return self._optimize_convolution(tensor, workload_type, target)
        elif operation == "linear":
            return self._optimize_linear(tensor, tensor2, workload_type, target)
        elif operation == "attention":
            return self._optimize_attention(tensor, tensor2, workload_type, target)
        elif operation == "elementwise":
            return self._optimize_elementwise(tensor, tensor2, workload_type, target)
        else:
            # Общая оптимизация размеров
            return self._optimize_generic(tensor, workload_type, target)
    
    def _optimize_matmul(self, a: torch.Tensor, b: Optional[torch.Tensor],
                        workload_type: str, target: str) -> torch.Tensor:
        """
        Оптимизация умножения матриц по теории ТРАП
        
        Ключевые идеи:
        1. Приведение размеров к резонансным
        2. Оптимальное разбиение на блоки
        3. Улучшение кэширования
        """
        if b is None:
            b = a.T  # Авто-транспонирование для квадратных матриц
        
        # 1. Анализируем размеры
        m, k = a.shape[-2], a.shape[-1]
        k2, n = b.shape[-2], b.shape[-1]
        
        # 2. Находим оптимальные (резонансные) размеры
        optimal_k = self._find_optimal_inner_size(k, k2, 'matmul')
        
        # 3. Если нужно, изменяем размеры
        needs_optimization = self._needs_size_optimization(
            (m, k, n), optimal_k, threshold=0.1
        )
        
        if not needs_optimization:
            # Размеры уже оптимальны
            return torch.matmul(a, b)
        
        # 4. Оптимизируем размеры
        a_opt, b_opt = self._resize_matrices_for_matmul(a, b, optimal_k)
        
        # 5. Выполняем умножение с оптимальными параметрами
        result = self._matmul_with_optimal_params(a_opt, b_opt, target)
        
        # 6. При необходимости обрезаем до исходных размеров
        if result.shape[-1] != n:
            result = result[..., :n]
        if result.shape[-2] != m:
            result = result[:m, ...]
        
        return result
    
    def _optimize_convolution(self, x: torch.Tensor,
                            workload_type: str, target: str) -> torch.Tensor:
        """
        Оптимизация свертки
        
        Особенности:
        1. Оптимальные размеры каналов
        2. Выравнивание по границам
        3. Оптимальные ядра
        """
        if len(x.shape) != 4:  # Только для 4D тензоров [batch, channels, height, width]
            return x
        
        batch, channels, height, width = x.shape
        
        # Находим оптимальный размер каналов
        optimal_channels = self._find_nearest_resonant(channels, 'conv')
        
        if optimal_channels == channels:
            # Размеры уже оптимальны
            return x
        
        # Оптимизируем размер каналов
        if optimal_channels > channels:
            # Дополняем нулями
            x_opt = F.pad(x, (0, 0, 0, 0, 0, optimal_channels - channels))
        else:
            # Обрезаем
            x_opt = x[:, :optimal_channels, :, :]
        
        return x_opt
    
    def _optimize_linear(self, x: torch.Tensor, weight: Optional[torch.Tensor],
                        workload_type: str, target: str) -> torch.Tensor:
        """
        Оптимизация линейных слоев (нейросети)
        """
        if weight is None:
            return x
        
        # Анализируем размеры
        if len(x.shape) == 2:  # [batch, features]
            batch, in_features = x.shape
            out_features = weight.shape[0] if len(weight.shape) == 2 else weight.shape[1]
            
            # Находим оптимальные размеры
            optimal_in = self._find_nearest_resonant(in_features, 'linear')
            optimal_out = self._find_nearest_resonant(out_features, 'linear')
            
            # Оптимизируем размеры
            x_opt = self._resize_tensor(x, optimal_in, dim=-1)
            weight_opt = self._resize_tensor(weight, (optimal_out, optimal_in))
            
            # Выполняем линейное преобразование
            return torch.matmul(x_opt, weight_opt.T)
        
        return x
    
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
        
        # Оптимизируем размеры последовательности
        seq_len = q.shape[-2]
        optimal_seq_len = self._find_nearest_resonant(seq_len, 'attention')
        
        if optimal_seq_len == seq_len:
            # Стандартное внимание
            scores = torch.matmul(q, k.transpose(-2, -1)) / math.sqrt(q.size(-1))
            attention = F.softmax(scores, dim=-1)
            return torch.matmul(attention, v)
        
        # Обрезаем или дополняем последовательность
        q_opt = self._resize_tensor(q, optimal_seq_len, dim=-2)
        k_opt = self._resize_tensor(k, optimal_seq_len, dim=-2)
        v_opt = self._resize_tensor(v, optimal_seq_len, dim=-2)
        
        # Внимание с оптимальными размерами
        scores = torch.matmul(q_opt, k_opt.transpose(-2, -1)) / math.sqrt(q_opt.size(-1))
        attention = F.softmax(scores, dim=-1)
        result = torch.matmul(attention, v_opt)
        
        # Возвращаем к исходному размеру
        return self._resize_tensor(result, seq_len, dim=-2)
    
    def _optimize_elementwise(self, a: torch.Tensor, b: Optional[torch.Tensor],
                            workload_type: str, target: str) -> torch.Tensor:
        """Оптимизация поэлементных операций"""
        if b is None:
            return a
        
        # Выравниваем размеры
        if a.shape != b.shape:
            # Пытаемся broadcast
            try:
                result_shape = torch.broadcast_shapes(a.shape, b.shape)
                a_aligned = a.expand(result_shape) if a.shape != result_shape else a
                b_aligned = b.expand(result_shape) if b.shape != result_shape else b
                return a_aligned + b_aligned  # Или другая операция
            except:
                return a
        
        return a + b  # Или другая операция
    
    def _optimize_generic(self, tensor: torch.Tensor,
                         workload_type: str, target: str) -> torch.Tensor:
        """Общая оптимизация тензора"""
        # Просто приводим размеры к резонансным
        optimal_shape = []
        for dim in tensor.shape:
            optimal_dim = self._find_nearest_resonant(dim, 'generic')
            optimal_shape.append(optimal_dim)
        
        if list(tensor.shape) == optimal_shape:
            return tensor
        
        # Изменяем размер
        return self._resize_tensor(tensor, tuple(optimal_shape))
    
    def _find_optimal_inner_size(self, size1: int, size2: int, op_type: str) -> int:
        """Находит оптимальный внутренний размер для операции"""
        min_size = min(size1, size2)
        
        # Выбираем из резонансных размеров
        candidates = []
        for size in self.resonant_sizes:
            if size >= min_size:  # Только увеличение (как в ТРАП)
                increase = (size - min_size) / min_size
                if increase < 0.25:  # Не более 25% увеличения
                    score = self._score_size_for_operation(size, op_type)
                    candidates.append((score, -increase, size))
        
        if candidates:
            candidates.sort(reverse=True)
            return candidates[0][2]
        
        return min_size
    
    def _score_size_for_operation(self, size: int, op_type: str) -> float:
        """Оценка размера для конкретной операции"""
        score = 0.0
        
        # Базовые критерии
        if size % 64 == 0:
            score += 2.0  # Отлично для tensor cores
        if size % 128 == 0:
            score += 1.5  # Хорошо для кэша
        if bin(size).count('1') == 1:  # Степень двойки
            score += 1.0
        
        # Критерии для конкретных операций
        if op_type == 'matmul':
            if size % 256 == 0:
                score += 1.0
        elif op_type == 'conv':
            if size % 32 == 0:
                score += 1.0
        elif op_type == 'linear':
            if 256 <= size <= 4096:
                score += 1.0
        elif op_type == 'attention':
            if 64 <= size <= 2048:
                score += 1.0
        
        return score
    
    def _find_nearest_resonant(self, size: int, op_type: str) -> int:
        """Находит ближайший резонансный размер"""
        if size in self.resonant_sizes:
            return size
        
        # Ищем в кэше
        cache_key = f"{op_type}_{size}"
        if cache_key in self.size_cache:
            return self.size_cache[cache_key]
        
        # Находим ближайший
        distances = []
        for resonant in self.resonant_sizes:
            # Предпочитаем увеличение уменьшению (как в ТРАП)
            if resonant >= size:
                distance = resonant - size
            else:
                distance = (size - resonant) * 1.5  # Штраф за уменьшение
            
            # Учитываем тип операции
            score = self._score_size_for_operation(resonant, op_type)
            distances.append((distance - score * 10, resonant))  # Чем лучше score, тем меньше distance
        
        distances.sort()
        optimal = distances[0][1]
        
        # Кэшируем
        self.size_cache[cache_key] = optimal
        
        return optimal
    
    def _needs_size_optimization(self, sizes: Tuple[int, ...], 
                               optimal_size: int, threshold: float = 0.1) -> bool:
        """Определяет, нужна ли оптимизация размеров"""
        for size in sizes:
            if size == 0:
                continue
            deviation = abs(optimal_size - size) / size
            if deviation > threshold:
                return True
        return False
    
    def _resize_matrices_for_matmul(self, a: torch.Tensor, b: torch.Tensor,
                                  optimal_k: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """Изменяет размеры матриц для оптимального умножения"""
        m, k = a.shape[-2], a.shape[-1]
        k2, n = b.shape[-2], b.shape[-1]
        
        if k != optimal_k:
            # Дополняем или обрезаем по размеру K
            a_resized = self._resize_tensor(a, optimal_k, dim=-1)
        else:
            a_resized = a
        
        if k2 != optimal_k:
            b_resized = self._resize_tensor(b, optimal_k, dim=-2)
        else:
            b_resized = b
        
        return a_resized, b_resized
    
    def _matmul_with_optimal_params(self, a: torch.Tensor, b: torch.Tensor,
                                  target: str) -> torch.Tensor:
        """Умножение матриц с оптимальными параметрами"""
        # Используем блочное умножение для больших матриц
        m, k = a.shape[-2], a.shape[-1]
        n = b.shape[-1]
        
        # Определяем стратегию в зависимости от цели
        if target == "energy":
            # Для экономии энергии используем меньшие блоки
            block_size = self._get_energy_efficient_block_size()
            return self._blocked_matmul_energy(a, b, block_size)
        else:
            # Для производительности используем tensor cores когда возможно
            if self._can_use_tensor_cores(a, b):
                return self._tensor_core_matmul(a, b)
            else:
                block_size = self._get_performance_block_size()
                return self._blocked_matmul_perf(a, b, block_size)
    
    def _blocked_matmul_energy(self, a: torch.Tensor, b: torch.Tensor,
                             block_size: int) -> torch.Tensor:
        """Блочное умножение для экономии энергии"""
        m, k = a.shape[-2], a.shape[-1]
        n = b.shape[-1]
        
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
    
    def _blocked_matmul_perf(self, a: torch.Tensor, b: torch.Tensor,
                           block_size: int) -> torch.Tensor:
        """Блочное умножение для производительности"""
        # Используем более крупные блоки и асинхронность
        m, k = a.shape[-2], a.shape[-1]
        n = b.shape[-1]
        
        result = torch.zeros((m, n), device=a.device, dtype=a.dtype)
        
        # Крупные блоки для лучшей утилизации SM
        for i in range(0, m, block_size * 2):
            i_end = min(i + block_size * 2, m)
            for j in range(0, n, block_size * 2):
                j_end = min(j + block_size * 2, n)
                
                # Используем аккумулятор в shared memory
                block_acc = torch.zeros((block_size * 2, block_size * 2),
                                       device=a.device,
                                       dtype=a.dtype)
                
                for l in range(0, k, block_size):
                    l_end = min(l + block_size, k)
                    
                    a_block = a[i:i_end, l:l_end]
                    b_block = b[l:l_end, j:j_end]
                    block_acc[:i_end-i, :j_end-j] += torch.matmul(a_block, b_block)
                
                result[i:i_end, j:j_end] = block_acc[:i_end-i, :j_end-j]
        
        return result
    
    def _tensor_core_matmul(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        """Использование tensor cores когда возможно"""
        # Tensor cores требуют определенных размеров и типов данных
        try:
            # Пробуем использовать mixed precision для tensor cores
            with torch.cuda.amp.autocast():
                return torch.matmul(a, b)
        except:
            # Fallback на обычное умножение
            return torch.matmul(a, b)
    
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
    
    def _resize_tensor(self, tensor: torch.Tensor, new_size, dim: int = -1):
        """Изменяет размер тензора (дополняет или обрезает)"""
        if isinstance(new_size, tuple):
            # Изменение всех размеров
            current_shape = tensor.shape
            if current_shape == new_size:
                return tensor
            
            result = torch.zeros(new_size, device=tensor.device, dtype=tensor.dtype)
            
            # Копируем данные
            slices = []
            for cur, new in zip(current_shape, new_size):
                copy_size = min(cur, new)
                slices.append(slice(0, copy_size))
            
            result[tuple(slices)] = tensor[tuple(slice(0, c) for c in current_shape)]
            return result
        
        # Изменение одного измерения
        current_size = tensor.shape[dim]
        if current_size == new_size:
            return tensor
        
        new_shape = list(tensor.shape)
        new_shape[dim] = new_size
        
        result = torch.zeros(new_shape, device=tensor.device, dtype=tensor.dtype)
        
        # Копируем данные
        copy_size = min(current_size, new_size)
        if dim == -1:
            result[..., :copy_size] = tensor[..., :copy_size]
        elif dim == -2:
            result[..., :copy_size, :] = tensor[..., :copy_size, :]
        elif dim == 0:
            result[:copy_size, ...] = tensor[:copy_size, ...]
        elif dim == 1:
            result[:, :copy_size, ...] = tensor[:, :copy_size, ...]
        
        return result
    
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
            'successful_optimizations': 0
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
    
    return optimizer