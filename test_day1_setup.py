import torch
import time
import numpy as np

print("🚀 SIMPLE CUDA TEST FOR RTX 4070")
print("=" * 40)

# Test 1: Basic CUDA
print("1️⃣ CUDA Availability:")
cuda_available = torch.cuda.is_available()
print(f"   CUDA Available: {cuda_available}")

if cuda_available:
    print(f"   GPU Name: {torch.cuda.get_device_name(0)}")
    print(f"   GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    print(f"   CUDA Version: {torch.version.cuda}")
else:
    print("   ❌ CUDA not available!")
    exit()

# Test 2: Basic GPU Operations
print("\n2️⃣ GPU Performance Test:")
device = torch.device('cuda')

# Create test matrices
size = 2000
print(f"   Creating {size}x{size} matrices...")

# GPU test
start_time = time.time()
a_gpu = torch.randn(size, size, device=device)
b_gpu = torch.randn(size, size, device=device)
c_gpu = torch.matmul(a_gpu, b_gpu)
torch.cuda.synchronize()  # Wait for GPU to finish
gpu_time = time.time() - start_time

print(f"   GPU Time: {gpu_time:.3f} seconds")

# CPU test for comparison
start_time = time.time()
a_cpu = torch.randn(size, size)
b_cpu = torch.randn(size, size)
c_cpu = torch.matmul(a_cpu, b_cpu)
cpu_time = time.time() - start_time

print(f"   CPU Time: {cpu_time:.3f} seconds")
print(f"   GPU Speedup: {cpu_time/gpu_time:.1f}x faster!")

# Test 3: Memory Management
print("\n3️⃣ GPU Memory Test:")
memory_used = torch.cuda.memory_allocated() / 1e9
memory_cached = torch.cuda.memory_reserved() / 1e9
print(f"   Memory Used: {memory_used:.2f} GB")
print(f"   Memory Cached: {memory_cached:.2f} GB")

# Test 4: AI-like Operations
print("\n4️⃣ AI Operations Test:")
# Simulate neural network operations
batch_size = 32
features = 1000
hidden = 500

# Create fake data
x = torch.randn(batch_size, features, device=device)
w1 = torch.randn(features, hidden, device=device)
w2 = torch.randn(hidden, 1, device=device)

start_time = time.time()
for _ in range(100):  # 100 forward passes
    h = torch.relu(torch.matmul(x, w1))
    output = torch.sigmoid(torch.matmul(h, w2))
torch.cuda.synchronize()
ai_time = time.time() - start_time

print(f"   100 AI forward passes: {ai_time:.3f} seconds")
print(f"   Throughput: {100/ai_time:.1f} passes/second")

# Test 5: Multiple GPU Streams (Advanced)
print("\n5️⃣ Multi-Stream Test:")
try:
    stream1 = torch.cuda.Stream()
    stream2 = torch.cuda.Stream()
    
    with torch.cuda.stream(stream1):
        result1 = torch.matmul(a_gpu, b_gpu)
    
    with torch.cuda.stream(stream2):
        result2 = torch.matmul(b_gpu, a_gpu)
    
    torch.cuda.synchronize()
    print("   ✅ Multi-stream operations successful")
except Exception as e:
    print(f"   ⚠️ Multi-stream test failed: {e}")

del a_gpu, b_gpu, c_gpu, a_cpu, b_cpu, c_cpu
torch.cuda.empty_cache()

print("\n🎯 RESULTS:")
print("=" * 40)
if gpu_time < 1.0:
    print("✅ GPU Performance: EXCELLENT")
elif gpu_time < 2.0:
    print("✅ GPU Performance: GOOD")
else:
    print("⚠️ GPU Performance: Could be better")

if memory_used < 2.0:
    print("✅ Memory Usage: Efficient")
else:
    print("⚠️ Memory Usage: High")

print(f"\n🚀 Your RTX 4070 is ready for AI workloads!")
print("✅ CUDA setup complete - ready for Day 2!")