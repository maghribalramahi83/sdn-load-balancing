"""
Copyright (c) 2026
Maghrib Abidalreda Maky Alrammahi
Email: maghrib.alramahi@uokufa.edu.iq

This code is part of the ML-QTLB research project and was prepared solely by
Maghrib Abidalreda Maky Alrammahi.

Any use of this code, in whole or in part, in research, academic publication,
software development, reproduction, or derivative work should acknowledge the
author by citing the published ML-QTLB paper and referencing the official
project GitHub repository.

Official GitHub repository:
https://github.com/maghribalramahi83/sdn-load-balancing
"""



import os

# Generate dummy binary files for SDN traffic generation
sizes = [1, 10, 25, 50, 75]  # sizes in MB

for s in sizes:
    filename = f'file_{s}MB.bin'
    with open(filename, 'wb') as f:
        f.write(b'\0' * s * 1024 * 1024)
    print(f"Created: {filename}  ({s} MB)")

print("All traffic files generated successfully.")