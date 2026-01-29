import torch
import numpy as np
import time
from typing import Tuple, List, Dict, Any
import subprocess

class GPURingOptimizer:
    """
    GPU Optimizer using Ring Theory patterns - CORRECTED VERSION
    """
    
    def __init__(self, device: str = "cuda:0"):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.resonant_sizes = self._get_optimal_sizes()
        
    def _get_optimal_sizes(self) -> List[int]:
        """Get sizes that show resonance in experiments"""
        # From your experiments: sizes showing optimal patterns
        return [25, 50, 100, 200, 400, 800, 1600]
    
    def optimize_matmul(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        """
        MATHEMATICALLY CORRECT matrix multiplication with ring theory optimizations
        """
        # 1. Ensure tensors are 2D
        if a.dim() != 2 or b.dim() != 2:
            raise ValueError("Tensors must be 2D for matrix multiplication")
        
        # 2. Get dimensions
        m, k = a.shape
        k2, n = b.shape
        
        if k != k2:
            raise ValueError(f"Incompatible shapes: {a.shape} @ {b.shape}")
        
        # 3. Pad to resonant size if needed (для лучшего использования кэша)
        optimal_m = self._find_nearest_resonant(m)
        optimal_n = self._find_nearest_resonant(n)
        optimal_k = self._find_nearest_resonant(k)
        
        # 4. Если размеры близки к резонансным - используем стандартное умножение
        # с оптимальными параметрами запуска CUDA ядра
        if self._should_pad(m, optimal_m) or self._should_pad(n, optimal_n) or self._should_pad(k, optimal_k):
            return self._optimized_matmul_with_padding(a, b, optimal_m, optimal_n, optimal_k)
        else:
            # Размеры уже оптимальны - используем стандартное умножение
            # с настройкой параметров CUDA
            return self._optimized_cuda_matmul(a, b)
    
    def _optimized_cuda_matmul(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        """
        Standard matmul with CUDA optimization parameters
        """
        # Определяем оптимальные размеры блоков и гридов
        # на основе ваших экспериментальных данных
        m, k = a.shape
        k2, n = b.shape
        
        # Для РЕЗОНАНСНЫХ размеров из ваших экспериментов:
        # Размеры, показывающие паттерн ~1.65 Гц: 25, 100, 200
        # Размеры, показывающие паттерн ~3.6 Гц: 50, 400, 800
        
        # Проверяем, является ли текущий размер резонансным
        size_category = self._classify_size(m, n)
        
        if size_category == "low_freq":  # ~1.65 Гц паттерн
            # Для низкочастотных паттернов используем более агрессивную тайлинг
            return self._tiled_matmul(a, b, tile_size=32)
        else:  # ~3.6 Гц паттерн или другие
            # Для высокочастотных паттернов используем другой подход
            return self._tiled_matmul(a, b, tile_size=64)
    
    def _tiled_matmul(self, a: torch.Tensor, b: torch.Tensor, tile_size: int = 32) -> torch.Tensor:
        """
        Tiled matrix multiplication (better cache utilization)
        """
        m, k = a.shape
        k2, n = b.shape
        
        result = torch.zeros(m, n, device=a.device, dtype=a.dtype)
        
        # Tile the computation
        for i in range(0, m, tile_size):
            i_end = min(i + tile_size, m)
            for j in range(0, n, tile_size):
                j_end = min(j + tile_size, n)
                for l in range(0, k, tile_size):
                    l_end = min(l + tile_size, k)
                    
                    # Extract tiles
                    a_tile = a[i:i_end, l:l_end]
                    b_tile = b[l:l_end, j:j_end]
                    
                    # Compute tile
                    tile_result = torch.matmul(a_tile, b_tile)
                    
                    # Accumulate to result
                    result[i:i_end, j:j_end] += tile_result
        
        return result
    
    def _optimized_matmul_with_padding(self, a: torch.Tensor, b: torch.Tensor, 
                                      target_m: int, target_n: int, target_k: int) -> torch.Tensor:
        """
        Pad matrices to optimal sizes, multiply, then crop back
        """
        m, k = a.shape
        k2, n = b.shape
        
        # Pad if smaller than optimal
        if m < target_m or k < target_k:
            a_padded = self._pad_to_size(a, target_m, target_k)
        else:
            a_padded = a
            
        if k2 < target_k or n < target_n:
            b_padded = self._pad_to_size(b, target_k, target_n)
        else:
            b_padded = b
        
        # Perform optimized multiplication
        result_padded = self._optimized_cuda_matmul(a_padded, b_padded)
        
        # Crop back to original size
        return result_padded[:m, :n]
    
    def _pad_to_size(self, tensor: torch.Tensor, target_rows: int, target_cols: int) -> torch.Tensor:
        """Pad tensor to target size with zeros"""
        rows, cols = tensor.shape
        padded = torch.zeros(target_rows, target_cols, 
                            device=tensor.device, 
                            dtype=tensor.dtype)
        padded[:rows, :cols] = tensor
        return padded
    
    def _find_nearest_resonant(self, size: int) -> int:
        """Find nearest resonant size from experimental data"""
        # Ваши экспериментальные данные показывают два кластера:
        # Низкая частота (~1.65 Гц): 25, 100, 200, 1600
        # Высокая частота (~3.6 Гц): 50, 400, 800
        
        resonant_sizes = [25, 50, 100, 200, 400, 800, 1600]
        
        # Если размер уже близок к резонансному, не меняем
        for rs in resonant_sizes:
            if abs(size - rs) <= size * 0.1:  # В пределах 10%
                return rs
        
        # Иначе ищем ближайший
        return min(resonant_sizes, key=lambda x: abs(x - size))
    
    def _should_pad(self, current: int, optimal: int) -> bool:
        """Determine if padding is beneficial"""
        # Не паддим если:
        # 1. Текущий размер уже оптимальный
        # 2. Разница менее 5%
        # 3. Увеличение будет слишком большим (>50%)
        
        if current == optimal:
            return False
        
        diff = abs(optimal - current)
        ratio = optimal / current
        
        # Паддим только если:
        # - Разница значительная (>10%)
        # - Не увеличиваем слишком сильно (<1.5x)
        return diff > current * 0.1 and ratio < 1.5
    
    def _classify_size(self, m: int, n: int) -> str:
        """Classify matrix size based on experimental frequency patterns"""
        avg_size = (m + n) / 2
        
        # Из ваших экспериментов:
        low_freq_sizes = [25, 100, 200, 1600]  # ~1.65 Гц
        high_freq_sizes = [50, 400, 800]       # ~3.6 Гц
        
        # Находим ближайший резонансный размер
        resonant_sizes = low_freq_sizes + high_freq_sizes
        nearest = min(resonant_sizes, key=lambda x: abs(x - avg_size))
        
        if nearest in low_freq_sizes:
            return "low_freq"
        else:
            return "high_freq"
    
    def optimize_tensor_operation(self, tensor: torch.Tensor, operation: str = "matmul") -> torch.Tensor:
        """
        Main optimization interface - CORRECTED
        """
        if operation == "matmul":
            # Для matmul нужны два тензора
            # Создаем тестовый второй тензор того же размера
            b = torch.randn_like(tensor)
            return self.optimize_matmul(tensor, b)
        elif operation == "conv":
            return self._optimized_convolution(tensor)
        else:
            return tensor
    
    def _optimized_convolution(self, x: torch.Tensor) -> torch.Tensor:
        """
        Optimized convolution using ring patterns
        """
        if x.dim() != 4:
            return x
        
        # Используем резонансные размеры для настройки параметров свертки
        batch, channels, height, width = x.shape
        
        # Определяем оптимальный размер ядра на основе размеров
        optimal_kernel = self._determine_optimal_kernel_size(height, width)
        
        # Создаем ядро свертки
        kernel_size = optimal_kernel
        padding = kernel_size // 2
        
        weight = torch.ones(channels, channels, kernel_size, kernel_size,
                           device=x.device) / (kernel_size ** 2 * channels)
        
        # Выполняем свертку
        return torch.nn.functional.conv2d(x, weight, padding=padding)
    
    def _determine_optimal_kernel_size(self, height: int, width: int) -> int:
        """Determine optimal convolution kernel size based on dimensions"""
        avg_dim = (height + width) // 2
        
        # Маппинг размеров на оптимальные ядра из экспериментов
        if avg_dim <= 100:
            return 3  # Малые матрицы - маленькое ядро
        elif avg_dim <= 400:
            return 5  # Средние матрицы
        else:
            return 7  # Крупные матрицы
    
    def benchmark_optimization(self, size: int, iterations: int = 100) -> Dict[str, Any]:
        """
        Benchmark the optimization for specific size
        """
        # Create test matrices
        a = torch.randn(size, size, device=self.device)
        b = torch.randn(size, size, device=self.device)
        
        # Standard matmul benchmark
        torch.cuda.synchronize() if torch.cuda.is_available() else None
        start = time.time()
        for _ in range(iterations):
            standard = torch.matmul(a, b)
        torch.cuda.synchronize() if torch.cuda.is_available() else None
        std_time = time.time() - start
        
        # Optimized matmul benchmark
        torch.cuda.synchronize() if torch.cuda.is_available() else None
        start = time.time()
        for _ in range(iterations):
            optimized = self.optimize_matmul(a, b)
        torch.cuda.synchronize() if torch.cuda.is_available() else None
        opt_time = time.time() - start
        
        # Verify correctness
        if size <= 100:  # Для больших размеров проверка точности может быть дорогой
            mse = torch.mean((standard - optimized) ** 2).item()
        else:
            # Для больших матриц проверяем только подматрицу
            mse = torch.mean((standard[:100, :100] - optimized[:100, :100]) ** 2).item()
        
        return {
            "size": size,
            "standard_time": std_time,
            "optimized_time": opt_time,
            "speedup": std_time / opt_time if opt_time > 0 else 0,
            "mse_error": mse,
            "correct": mse < 1e-6  # Практически точное совпадение
        }


# Тестирующий код
def test_correctness():
    print("=" * 70)
    print("ТЕСТИРОВАНИЕ КОРРЕКТНОСТИ ОПТИМИЗАТОРА")
    print("=" * 70)
    
    optimizer = GPURingOptimizer()
    
    # Тест на маленькой матрице
    print("\n1. Тест на матрице 10x10:")
    a = torch.randn(10, 10, device=optimizer.device)
    b = torch.randn(10, 10, device=optimizer.device)
    
    # Стандартное умножение
    correct = torch.matmul(a, b)
    
    # Оптимизированное умножение
    optimized = optimizer.optimize_matmul(a, b)
    
    # Проверка
    mse = torch.mean((correct - optimized) ** 2).item()
    print(f"   MSE ошибка: {mse:.8f}")
    print(f"   Матрицы равны: {torch.allclose(correct, optimized, rtol=1e-5)}")
    
    # Показываем разницу
    print(f"   Максимальная разница: {torch.max(torch.abs(correct - optimized)).item():.6f}")
    
    if mse < 1e-6:
        print("   ✅ ТЕСТ ПРОЙДЕН! Математическая корректность обеспечена.")
    else:
        print("   ❌ ОШИБКА! Метод не сохраняет математическую корректность.")
    
    # Тест на резонансных размерах
    print("\n2. Тест на резонансных размерах из экспериментов:")
    test_sizes = [25, 50, 100, 200]
    
    for size in test_sizes:
        print(f"\n   Размер {size}x{size}:")
        a = torch.randn(size, size, device=optimizer.device)
        b = torch.randn(size, size, device=optimizer.device)
        
        correct = torch.matmul(a, b)
        optimized = optimizer.optimize_matmul(a, b)
        
        mse = torch.mean((correct - optimized) ** 2).item()
        print(f"     MSE: {mse:.8f}")
        print(f"     Корректно: {'✅' if mse < 1e-6 else '❌'}")
    
    print("\n" + "=" * 70)
    print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 70)

if __name__ == "__main__":
    test_correctness()