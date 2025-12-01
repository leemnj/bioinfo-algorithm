import sys
from collections import Counter

# ==========================================
# 1. 점수 계산 및 스펙트럼 생성 함수들 (Helpers)
# ==========================================

def get_linear_spectrum(peptide):
    """펩타이드(리스트)로부터 선형 스펙트럼 생성"""
    prefix_mass = [0]
    for mass in peptide:
        prefix_mass.append(prefix_mass[-1] + mass)
    
    linear_spectrum = [0]
    for i in range(len(peptide)):
        for j in range(i + 1, len(peptide) + 1):
            linear_spectrum.append(prefix_mass[j] - prefix_mass[i])
    return sorted(linear_spectrum)

def get_cyclic_spectrum(peptide):
    """펩타이드(리스트)로부터 고리형 스펙트럼 생성"""
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

def score_linear(peptide, spectrum_counter):
    """선형 점수 계산 (가지치기용)"""
    pep_spec = get_linear_spectrum(peptide)
    pep_counter = Counter(pep_spec)
    
    score = 0
    for mass, count in pep_counter.items():
        if mass in spectrum_counter:
            score += min(count, spectrum_counter[mass])
    return score

def score_cyclic(peptide, spectrum_counter):
    """고리형 점수 계산 (최종 확인용)"""
    pep_spec = get_cyclic_spectrum(peptide)
    pep_counter = Counter(pep_spec)
    
    score = 0
    for mass, count in pep_counter.items():
        if mass in spectrum_counter:
            score += min(count, spectrum_counter[mass])
    return score

# ==========================================
# 2. 핵심 알고리즘 함수들
# ==========================================

def get_convolution_alphabet(spectrum, M):
    """
    Spectral Convolution:
    스펙트럼의 모든 차이값을 구하고, 빈도수 상위 M개를 아미노산 후보로 선정
    """
    # 0이 없으면 추가 (차이값 계산의 정확도를 위해)
    spec_for_conv = sorted(spectrum)
    if spec_for_conv[0] != 0:
        spec_for_conv = [0] + spec_for_conv
        
    diffs = []
    # 모든 쌍의 차이 계산
    for i in range(len(spec_for_conv)):
        for j in range(i):
            diff = spec_for_conv[i] - spec_for_conv[j]
            if 57 <= diff <= 200: # 아미노산 질량 범위
                diffs.append(diff)
    
    # 빈도수 계산
    diff_counts = Counter(diffs).most_common()
    
    if not diff_counts:
        return []
    
    # M번째 빈도수 확인 (동점자 처리를 위해)
    threshold_idx = min(M, len(diff_counts)) - 1
    min_count = diff_counts[threshold_idx][1]
    
    alphabet = []
    for mass, count in diff_counts:
        if count >= min_count:
            alphabet.append(mass)
        else:
            break
            
    return alphabet

def trim_leaderboard(leaderboard, spectrum_counter, N):
    """
    Leaderboard 자르기 (Linear Score 기준 상위 N개)
    """
    if len(leaderboard) <= N:
        return leaderboard
    
    # (점수, 펩타이드) 형태로 변환 후 점수 내림차순 정렬
    scored_peptides = []
    for p in leaderboard:
        s = score_linear(p, spectrum_counter)
        scored_peptides.append((s, p))
        
    scored_peptides.sort(key=lambda x: x[0], reverse=True)
    
    # N번째 점수(커트라인) 찾기
    threshold_score = scored_peptides[N-1][0]
    
    # 커트라인 이상인 펩타이드만 살림
    return [p for s, p in scored_peptides if s >= threshold_score]

def convolution_cyclopeptide_sequencing(M, N, spectrum):
    """
    메인 함수
    """
    spectrum.sort()
    parent_mass = max(spectrum)
    spectrum_counter = Counter(spectrum)
    
    # 1. 알파벳(후보 질량) 선정
    alphabet = get_convolution_alphabet(spectrum, M)
    
    # 2. 초기화
    leaderboard = [[]]
    leader_peptide = []
    leader_score = 0
    
    # 3. 탐색 시작
    while leaderboard:
        new_leaderboard = []
        
        for peptide in leaderboard:
            for mass in alphabet:
                new_peptide = peptide + [mass]
                current_mass = sum(new_peptide)
                
                # Case A: 질량이 Parent Mass와 같음 (완성 후보)
                if current_mass == parent_mass:
                    curr_score = score_cyclic(new_peptide, spectrum_counter)
                    if curr_score > leader_score:
                        leader_score = curr_score
                        leader_peptide = new_peptide
                    # 완성된 펩타이드는 더 이상 확장하지 않음
                
                # Case B: 질량이 아직 작음 (확장 후보)
                elif current_mass < parent_mass:
                    new_leaderboard.append(new_peptide)
        
        # 4. 가지치기 (Trim)
        leaderboard = trim_leaderboard(new_leaderboard, spectrum_counter, N)
        
    return leader_peptide

# ==========================================
# 3. 실행부
# ==========================================
if __name__ == "__main__":
    # 데이터 입력 부분
    input_str = """
    20
    60
    57 57 71 99 129 137 170 186 194 208 228 265 285 299 307 323 356 364 394 422 493
    """
    
    # 실제 파일 사용 시:
    try:
        with open("input/rosalind_ba4i.txt", "r") as f:
            lines = f.read().splitlines()
            M = int(lines[0])
            N = int(lines[1])
            spectrum = sorted([int(x) for x in lines[2].split()])
    except: 
    
        # 예제 데이터 파싱
        lines = input_str.strip().split('\n')
        M = int(lines[0].strip())
        N = int(lines[1].strip())
        spectrum = sorted([int(x) for x in lines[2].strip().split()])

    # 알고리즘 실행
    result = convolution_cyclopeptide_sequencing(M, N, spectrum)

    # 결과 출력
    result_str = "-".join(map(str, result))
    print(f"내 정답: {result_str}")
    
    # --- [검증] 점수 확인 ---
    # Sample Output과 점수가 같은지 비교해보세요
    sample_output = [99, 71, 137, 57, 72, 57]
    spec_counter = Counter(spectrum)
    
    my_score = score_cyclic(result, spec_counter)
    sample_score = score_cyclic(sample_output, spec_counter)
    
    print(f"내 정답 점수: {my_score}")
    print(f"샘플 정답 점수: {sample_score}")
    
    if my_score == sample_score:
        print(">> 점수가 같습니다! Rosalind에서 정답 처리됩니다.")
    else:
        print(">> 점수가 다릅니다. 로직을 다시 확인해야 합니다.")