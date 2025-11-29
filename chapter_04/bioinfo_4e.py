# BA4E: Cyclipeptide Sequencing
import sys
from collections import Counter

# 1. 아미노산 정수 질량 테이블 (가장 많이 쓰이는 18개)
AMINO_ACID_MASSES = [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]

def get_linear_spectrum(peptide):
    """
    주어진 펩타이드(리스트)의 선형 스펙트럼을 구합니다.
    """
    prefix_mass = [0]
    for mass in peptide:
        prefix_mass.append(prefix_mass[-1] + mass)
    
    linear_spectrum = [0]
    for i in range(len(peptide)):
        for j in range(i + 1, len(peptide) + 1):
            linear_spectrum.append(prefix_mass[j] - prefix_mass[i])
            
    return sorted(linear_spectrum)

def get_cyclic_spectrum(peptide):
    """
    주어진 펩타이드(리스트)의 고리형 스펙트럼을 구합니다.
    """
    prefix_mass = [0]
    for mass in peptide:
        prefix_mass.append(prefix_mass[-1] + mass)
    
    peptide_mass = prefix_mass[-1]
    cyclic_spectrum = [0]
    
    for i in range(len(peptide)):
        for j in range(i + 1, len(peptide) + 1):
            sub_mass = prefix_mass[j] - prefix_mass[i]
            cyclic_spectrum.append(sub_mass)
            if i > 0 and j < len(peptide):
                cyclic_spectrum.append(peptide_mass - sub_mass)
                
    return sorted(cyclic_spectrum)

def is_consistent(peptide, spectrum_counter):
    """
    Branch and Bound의 핵심:
    현재 펩타이드의 선형 스펙트럼이 주어진 스펙트럼(Counter)에 포함되는지 확인합니다.
    """
    linear_spec = get_linear_spectrum(peptide)
    linear_counter = Counter(linear_spec)
    
    # 선형 스펙트럼의 각 질량 개수가 입력 스펙트럼보다 많으면 모순(False)
    for mass, count in linear_counter.items():
        if spectrum_counter[mass] < count:
            return False
    return True

def solve_cyclopeptide_sequencing(spectrum):
    parent_mass = max(spectrum)
    spectrum_counter = Counter(spectrum)
    
    # 후보 펩타이드 리스트 (초기값: 빈 리스트)
    candidate_peptides = [[]]
    final_peptides = []
    
    while candidate_peptides:
        new_candidates = []
        
        for peptide in candidate_peptides:
            # 1. Branch: 각 후보에 18종의 아미노산을 붙여 확장
            for mass in AMINO_ACID_MASSES:
                new_peptide = peptide + [mass]
                current_mass = sum(new_peptide)
                
                # 2. Case Check
                if current_mass == parent_mass:
                    # 총 질량이 같으면 -> 고리형 스펙트럼이 일치하는지 확인 (정답 후보)
                    if get_cyclic_spectrum(new_peptide) == spectrum:
                        final_peptides.append(new_peptide)
                    # 질량이 꽉 찼으므로 더 이상 확장하지 않음 (Drop)
                
                elif current_mass < parent_mass:
                    # 질량이 아직 부족하면 -> 선형 스펙트럼 일관성 검사 (Bound)
                    if is_consistent(new_peptide, spectrum_counter):
                        new_candidates.append(new_peptide)
                    # 일관성이 없으면 버림 (Pruning)
        
        candidate_peptides = new_candidates

    return final_peptides

# --- 실행부 ---
if __name__ == "__main__":
    # 데이터 입력 (Rosalind 예제 데이터)
    # 실제 파일 경로가 있다면 아래처럼 읽어오세요.
    try:
        with open("input/rosalind_ba4e.txt", "r") as f:
            input_str = f.read().strip()
    except:
        # 예시 입력 (Rosalind Sample Dataset)
        input_str = "0 113 128 186 241 299 314 427"
    
    # 입력 처리
    spectrum = sorted([int(x) for x in input_str.split()])
    
    # 알고리즘 실행
    results = solve_cyclopeptide_sequencing(spectrum)
    
    # 결과 포맷팅 (예: 113-128-186)
    # 중복 제거 (순서만 다른 동일 펩타이드들이 나올 수 있음)
    unique_results = []
    seen_str = set()
    
    for pep in results:
        # 하이픈(-)으로 연결된 문자열 생성
        pep_str = "-".join(map(str, pep))
        if pep_str not in seen_str:
            unique_results.append(pep_str)
            seen_str.add(pep_str)
            
    # Rosalind는 보통 공백으로 구분된 문자열 리스트를 요구함
    print(*unique_results)