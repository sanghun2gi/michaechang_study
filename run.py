#!/usr/bin/env python3
"""
Korean Road GPS Analysis Pipeline
실행: python run.py
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from generate_data import generate, OUTPUT_DIR as DATA_DIR
from analyze import main as run_analysis

if __name__ == '__main__':
    # Step 1: Generate sample NMEA data (300 files)
    print('▶ STEP 1 — 샘플 NMEA 데이터 생성 (300개)')
    generate(300)

    # Step 2: Analyze patterns & create visualizations
    print('\n▶ STEP 2 — 패턴 분석 + 시각화')
    run_analysis()
