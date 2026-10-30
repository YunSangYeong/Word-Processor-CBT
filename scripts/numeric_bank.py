"""29 explicitly disclosed arithmetic families, 20 fixed conditions per family.

Authoring uses exact rational arithmetic. Verification is implemented separately
in TypeScript, including inverse checks and discrete allocation simulations.
No external source or past-exam provenance is asserted.
"""
from fractions import Fraction

SUBJECTS = ['워드프로세싱 용어 및 기능', 'PC 운영체제', 'PC 기본상식']
FAMILIES = []

def family(subject, key, title, unit, precision=0):
    items = []
    FAMILIES.append(dict(subject=SUBJECTS[subject-1], key=key, title=title,
                         unit=unit, precision=precision, items=items))
    return items

def add(items, values, question, result, explanation):
    items.append(dict(values=values, question=question, result=Fraction(result), explanation=explanation))

def ceiling(value):
    value = Fraction(value)
    return -(-value.numerator // value.denominator)


def format_number(value):
    value = Fraction(value)
    if value.denominator == 1:
        return str(value.numerator)
    # Every authored non-integral result is an exact multiple of 0.1.
    assert (value * 10).denominator == 1
    return f'{float(value):.1f}'


def definitions():
    FAMILIES.clear()
    a = family(1, 'printable-width', '쪽의 본문 가로 폭', 'mm')
    for i in range(20):
        width, left, right = 210, 10+i%5, 10+2*(i//5)
        answer = width-left-right
        add(a,[width,left,right],f'폭 {width}mm 용지에서 왼쪽 여백 {left}mm, 오른쪽 여백 {right}mm를 제외한다. 제본 여백 등 다른 가로 여백이 없을 때 본문 가로 폭은?',answer,
            f'본문 가로 폭은 용지 폭에서 좌우 여백을 뺀다. {width}−{left}−{right}={answer}mm이다. 제본 여백이나 단 나누기는 없다는 조건이며 프린터의 별도 인쇄 불가 영역은 계산에 포함하지 않는다.')
    a = family(1, 'printable-height', '쪽의 본문 세로 높이', 'mm')
    for i in range(20):
        height, top, bottom = 297, 15+i, 12+i%4
        answer = height-top-bottom
        add(a,[height,top,bottom],f'높이 {height}mm 용지의 위 여백은 {top}mm, 아래 여백은 {bottom}mm이다. 머리말·꼬리말이 본문 공간을 추가로 차지하지 않을 때 본문 세로 높이는?',answer,
            f'본문 세로 높이는 용지 높이에서 위아래 여백을 제외해 구한다. {height}−{top}−{bottom}={answer}mm이다. 추가 영역이 없다는 문제 조건에 따른 결과다.')
    a = family(1, 'column-width', '다단의 한 단 너비', 'mm')
    for i in range(20):
        columns, gap = 2+i%2, 4+2*(i%3)
        width = columns*(55+i)+gap*(columns-1)
        answer = Fraction(width-gap*(columns-1),columns)
        add(a,[width,columns,gap],f'본문 폭 {width}mm를 너비가 같은 {columns}단으로 나눈다. 인접 단 사이 간격이 각각 {gap}mm이고 다른 구분 영역이 없을 때 한 단의 너비는?',answer,
            f'{columns}개 단 사이의 간격은 {columns-1}개다. 전체 간격 {gap}×{columns-1}mm를 본문 폭에서 빼고 단 수로 나누면 ({width}−{gap}×{columns-1})÷{columns}={format_number(answer)}mm이다.')
    a = family(1, 'table-cell-width', '균등한 표 열 너비', 'mm')
    for i in range(20):
        columns = 3+i%4
        width = columns*(16+i)
        answer = Fraction(width,columns)
        add(a,[width,columns],f'전체 폭 {width}mm인 표를 같은 너비의 {columns}열로 만든다. 테두리 두께와 셀 간격은 무시할 때 각 열의 너비는?',answer,
            f'전체 폭을 같은 크기의 열 수로 나누면 된다. {width}÷{columns}={format_number(answer)}mm이다. 테두리·셀 간격을 제외한다는 조건이며 셀 안쪽 여백은 별도의 텍스트 배치 속성이다.')
    a = family(1, 'first-line-position', '첫 줄의 절대 시작 위치', 'mm')
    for i in range(20):
        margin, indent, first = 15+i%3, 5+i%5, 2+i//5
        answer = margin+indent+first
        add(a,[margin,indent,first],f'용지 왼쪽 끝부터 여백이 {margin}mm이다. 본문 왼쪽 경계 기준 문단 들여쓰기는 {indent}mm, 그 문단의 기본 위치에서 첫 줄을 추가로 {first}mm 들여쓴다. 첫 줄의 용지 왼쪽 끝 기준 시작 위치는?',answer,
            f'같은 오른쪽 방향 거리이므로 여백·문단 들여쓰기·추가 첫 줄 들여쓰기를 더한다. {margin}+{indent}+{first}={answer}mm이다. 내어쓰기나 양방향 문서가 아닌 명시한 좌표 조건이다.')
    a = family(1, 'text-page-count', '고정 행 수의 최소 쪽 수', '쪽')
    for i in range(20):
        lines, per_page = 81+17*i, 25+i%4
        answer = ceiling(Fraction(lines,per_page))
        add(a,[lines,per_page],f'총 {lines}줄을 한 쪽에 최대 {per_page}줄씩 순서대로 배치한다. 별도 제목·빈 쪽·문단 보호 조건은 없다. 필요한 최소 쪽 수는?',answer,
            f'줄 수를 쪽당 최대 줄 수로 나눈 뒤 남는 줄이 있으면 한 쪽이 더 필요하다. ceil({lines}÷{per_page})={answer}쪽이다. 나머지를 버리거나 반올림하지 않고 올림한다.')
    a = family(1, 'simplex-copies', '단면 인쇄 부수와 용지 수', '장')
    for i in range(20):
        pages, copies = 5+i, 2+i%5
        answer = pages*copies
        add(a,[pages,copies],f'{pages}쪽 문서를 {copies}부 단면 인쇄한다. 한 면에 한 쪽씩, 표지나 실패 출력 없이 인쇄할 때 필요한 용지는?',answer,
            f'단면으로 한 쪽당 한 장을 쓰므로 문서 쪽 수에 부수를 곱한다. {pages}×{copies}={answer}장이다. 여러 쪽 모아 찍기와 양면 인쇄는 사용하지 않는 조건이다.')
    a = family(1, 'duplex-copies', '양면 인쇄의 부별 올림', '장')
    for i in range(20):
        pages, copies = 9+2*i, 2+i%4
        answer = ceiling(Fraction(pages,2))*copies
        add(a,[pages,copies],f'{pages}쪽 문서를 {copies}부 양면 인쇄한다. 각 부는 반드시 새 용지 앞면에서 시작하고 한 면에 한 쪽만 인쇄한다. 추가 표지·실패 출력이 없을 때 최소 용지 수는?',answer,
            f'한 부에 ceil({pages}÷2)={ceiling(Fraction(pages,2))}장이 필요하다. 부 사이에 남는 뒷면을 공유하지 않으므로 이를 {copies}배 한다. 결과는 {answer}장이다. 전체 쪽 수를 한 번에 나누면 부별 시작 조건을 놓칠 수 있다.')
    a = family(1, 'font-print-scale', '인쇄 배율과 글자 크기', 'pt')
    for i in range(20):
        size, percent = 10+2*i, 50+50*(i%4)
        answer = Fraction(size*percent,100)
        add(a,[size,percent],f'문서의 글자 크기가 {size}pt이다. 실제 출력 길이에 {percent}%의 균일 인쇄 배율이 적용되고 다른 축소가 없다면 출력 글자 크기에 해당하는 값은?',answer,
            f'균일 인쇄 배율은 길이에 비례한다. {size}×({percent}÷100)={format_number(answer)}pt이다. 화면 보기 배율이 아니라 실제 인쇄 배율이라는 조건에 유의한다.')
    a = family(1, 'raster-print-width', '그림 화소 수와 인쇄 폭', '인치',1)
    for i in range(20):
        pixels, ppi = 900+90*i, 300
        answer = Fraction(pixels,ppi)
        add(a,[pixels,ppi],f'가로 {pixels}픽셀인 래스터 그림을 가로 방향 {ppi}ppi(1인치당 픽셀 수)로 배치한다. 재표본화와 추가 배율이 없을 때 가로 인쇄 폭은? 소수 첫째 자리까지 표시한다.',answer,
            f'가로 인쇄 폭은 가로 픽셀 수를 1인치당 픽셀 수로 나눈 값이다. {pixels}÷{ppi}={format_number(answer)}인치이다. PPI는 그림 화소 밀도이며 프린터의 잉크 점 수와 구별한다.')

    a = family(2, 'files-total', '같은 크기 파일의 총 데이터량', 'KiB')
    for i in range(20):
        size, files = 16+i, 3+i%5
        answer = size*files
        add(a,[size,files],f'각각 {size}KiB인 파일 {files}개의 논리적 파일 크기 합은? 메타데이터·클러스터 반올림·압축은 계산하지 않는다.',answer,
            f'같은 크기 파일의 개수에 파일당 크기를 곱한다. {size}×{files}={answer}KiB이다. 실제 디스크 점유량과 논리적 파일 크기는 클러스터와 메타데이터 때문에 다를 수 있다.')
    a = family(2, 'kib-to-bytes', '이진 용량 단위 변환', '바이트')
    for i in range(20):
        kib = 12+13*i
        answer = kib*1024
        add(a,[kib],f'파일의 논리적 크기가 {kib}KiB이다. 1KiB=1024바이트로 계산할 때 바이트 수는?',answer,
            f'이진 접두사 KiB의 정의를 사용해 {kib}×1024={answer}바이트로 바꾼다. 십진 KB=1000바이트와 혼동하지 않으며 디스크 할당 단위는 계산하지 않는다.')
    a = family(2, 'cluster-count', '파일 할당 클러스터 수', '개')
    for i in range(20):
        size, cluster = 5000+1379*i, 4096
        answer = ceiling(Fraction(size,cluster))
        add(a,[size,cluster],f'파일 크기가 {size}바이트이고 클러스터 하나는 {cluster}바이트다. 파일이 별도 클러스터를 온전히 할당받고 압축·희소 저장·상주 데이터는 없을 때 필요한 최소 클러스터 수는?',answer,
            f'파일은 클러스터의 일부만 사용해도 그 클러스터가 할당된다. ceil({size}÷{cluster})={answer}개이다. 실제 파일 시스템의 별도 메타데이터 영역은 이 계산에서 제외한다.')
    a = family(2, 'cluster-slack', '마지막 클러스터의 남는 공간', '바이트')
    for i in range(20):
        size, cluster = 6500+1481*i, 4096
        allocated = ceiling(Fraction(size,cluster))*cluster
        answer = allocated-size
        add(a,[size,cluster],f'{size}바이트 파일에 {cluster}바이트 클러스터를 필요한 최소 개수만큼 할당한다. 다른 파일과 클러스터를 공유하지 않으며 압축·희소 저장은 없다. 할당 공간에서 파일 데이터를 제외한 남는 바이트 수는?',answer,
            f'필요 클러스터 수는 ceil({size}÷{cluster})={allocated//cluster}개다. 할당 크기 {allocated}바이트에서 파일 크기 {size}바이트를 빼면 {answer}바이트이다. 메타데이터는 제외한 내부 단편화 계산이다.')
    a = family(2, 'volume-free', '볼륨의 남은 논리 용량', 'MiB')
    for i in range(20):
        total, used = 2048+256*i, 300+23*i
        answer = total-used
        add(a,[total,used],f'논리 용량 {total}MiB인 볼륨에서 사용량이 {used}MiB로 표시된다. 예약·메타데이터 등도 이 사용량에 모두 포함돼 있고 다른 예약 공간은 없을 때 남은 용량은?',answer,
            f'같은 단위이므로 전체 용량에서 사용량을 뺀다. {total}−{used}={answer}MiB이다. 별도 예약량이 없다는 조건이며 실제 운영체제의 표시 방식과 구분한다.')
    a = family(2, 'full-incremental', '전체 및 증분 사본의 총 보관량', 'MiB')
    for i in range(20):
        full, inc, days = 1000+100*i, 20+3*i, 3+i%5
        answer = full+inc*days
        add(a,[full,inc,days],f'전체 백업 {full}MiB 한 개와 하루에 하나씩 {inc}MiB인 증분 백업 {days}개를 모두 보관한다. 압축·중복 제거·메타데이터는 없을 때 총 보관량은?',answer,
            f'전체 백업 한 개에 증분 사본들의 크기를 더한다. {full}+({inc}×{days})={answer}MiB이다. 증분 사슬 보관량이며 매번 전체 백업을 만드는 것으로 계산하지 않는다.')
    a = family(2, 'copy-time', '일정 복사율의 이론 시간', '초')
    for i in range(20):
        size, speed = 60+12*i, 6
        answer = Fraction(size,speed)
        add(a,[size,speed],f'{size}MiB 파일을 유효 속도 {speed}MiB/s로 처음부터 끝까지 일정하게 복사한다. 준비 시간과 추가 지연이 없을 때 걸리는 시간은?',answer,
            f'시간은 데이터 크기를 단위 시간당 전송량으로 나눈다. {size}÷{speed}={format_number(answer)}초이다. 양쪽에 같은 이진 단위를 사용하므로 단위가 소거된다. 실제 복사 속도 변동은 배제한 이론값이다.')
    a = family(2, 'compressed-size', '압축 후 남는 크기', 'MiB')
    for i in range(20):
        size, percent = 80+20*i, 25+25*(i%3)
        answer = Fraction(size*percent,100)
        add(a,[size,percent],f'원본 {size}MiB 파일이 압축 후 원본 크기의 {percent}%가 되었다. 이 비율에 모든 부가 정보가 포함되어 있을 때 압축 파일 크기는?',answer,
            f'압축 후 비율을 원본에 곱한다. {size}×{percent}÷100={format_number(answer)}MiB이다. 줄어든 비율이 아니라 남은 크기의 비율이라는 조건에 유의한다.')
    a = family(2, 'memory-pages', '주소 영역을 담는 페이지 수', '개')
    for i in range(20):
        size, page = 128+64*i, 4*(2**(i%3))
        answer = ceiling(Fraction(size,page))
        add(a,[size,page],f'가상 주소 영역 {size}KiB를 페이지당 {page}KiB 단위로 담는다. 영역은 페이지 경계에서 시작하고 다른 영역과 마지막 페이지를 공유하지 않는다. 필요한 최소 페이지 수는?',answer,
            f'페이지 경계에서 시작하므로 전체 크기를 페이지 크기로 나누고 나머지가 있으면 올림한다. ceil({size}÷{page})={answer}개다. 실제 물리 메모리에 모두 상주한다는 뜻은 아니다.')
    a = family(2, 'scheduled-elapsed', '같은 날 작업의 경과 시간', '분')
    for i in range(20):
        start = (8+i%8)*60+5+2*i
        end = start+25+3*i
        answer = end-start
        add(a,[start,end],f'백업 작업이 같은 날 {start//60:02}:{start%60:02}에 시작해 {end//60:02}:{end%60:02}에 끝났다. 날짜·시계·시간대 변경과 중단이 없을 때 실제 경과 시간은 몇 분인가?',answer,
            f'두 시각을 자정 이후 분으로 바꾸어 뺀다. 종료 {end}분−시작 {start}분={answer}분이다. 시간 부분과 분 부분을 따로 십진 소수처럼 계산하면 안 된다.')

    a = family(3, 'binary-value', '이진 정수의 십진 값', '(10진수)')
    for i in range(20):
        value = 17+7*i
        # Authoring path: positional expansion, not the independent verifier's parser.
        digits = f'{value:b}'
        answer = sum(int(bit)*2**power for power,bit in enumerate(reversed(digits)))
        add(a,[value],f'부호 없는 2진수 {digits}를 10진수로 바꾸면?',answer,
            f'2진수는 오른쪽부터 1, 2, 4, 8 등의 자릿값을 갖는다. 각 자리의 0 또는 1에 자릿값을 곱해 합하면 {digits}₂={answer}₁₀이다. 부호 비트나 소수점은 없는 조건이다.')
    a = family(3, 'hex-value', '십육진 정수의 십진 값', '(10진수)')
    for i in range(20):
        value = 31+13*i
        digits = f'{value:X}'
        answer = sum(int(digit,16)*16**power for power,digit in enumerate(reversed(digits)))
        add(a,[value],f'부호 없는 16진수 {digits}를 10진수로 바꾸면? A~F는 각각 10~15이다.',answer,
            f'16진수는 오른쪽부터 1, 16, 256 등의 자릿값을 갖는다. 각 숫자에 해당 자릿값을 곱해 합하면 {digits}₁₆={answer}₁₀이다. 문자 A~F는 10~15를 나타낸다.')
    a = family(3, 'bit-patterns', '비트 패턴의 개수', '가지')
    for i in range(20):
        bits = 3+i
        answer = 2**bits
        add(a,[bits],f'{bits}개의 비트를 각각 독립적으로 0 또는 1로 정한다. 모든 비트를 사용하며 예약 패턴이 없을 때 가능한 서로 다른 비트 패턴 수는?',answer,
            f'비트 하나마다 선택이 두 가지이고 각 선택이 독립이므로 2를 비트 수만큼 곱한다. 2^{bits}={answer}가지다. 표현 가능한 값의 개수이며 최댓값과는 1 차이가 난다.')
    a = family(3, 'network-time', '비트율과 바이트량의 전송 시간', '초',1)
    for i in range(20):
        size, speed = 1500000+300000*i, 2000000
        answer = Fraction(size*8,speed)
        add(a,[size,speed],f'{size}바이트를 유효 속도 {speed}bit/s로 일정하게 보낸다. 1바이트=8비트이며 헤더·재전송·대기 시간은 없다. 걸리는 시간은? 소수 첫째 자리까지 표시한다.',answer,
            f'바이트 수를 비트로 바꾼 뒤 비트율로 나눈다. ({size}×8)÷{speed}={format_number(answer)}초이다. 여기서 속도는 bit/s이며 바이트/s가 아니라는 점에 유의한다.')
    a = family(3, 'rgb-bytes', '무압축 RGB 화소 데이터량', '바이트')
    for i in range(20):
        width, height, depth = 100+20*i, 80+10*i, 24
        answer = width*height*depth//8
        add(a,[width,height,depth],f'{width}×{height}픽셀 그림의 각 픽셀은 RGB 합계 {depth}비트로 저장된다. 압축·알파·헤더·팔레트·행 패딩이 없는 조밀한 화소 데이터의 바이트 수는?',answer,
            f'픽셀 수는 {width}×{height}이고 픽셀당 {depth}÷8=3바이트다. {width}×{height}×3={answer}바이트이다. 파일 헤더나 추가 채널은 제외하므로 실제 특정 파일 형식의 크기와는 다를 수 있다.')
    a = family(3, 'pcm-bytes', '무압축 PCM 음성 데이터량', '바이트')
    for i in range(20):
        rate, channels, depth, seconds = 8000+1000*i, 1+i%2, 16, 2+i%5
        answer = rate*channels*depth*seconds//8
        add(a,[rate,channels,depth,seconds],f'무압축 PCM 음성을 표본화율 {rate}Hz, {channels}채널, 채널당 표본 {depth}비트로 {seconds}초 저장한다. 헤더·패딩은 없을 때 음성 데이터의 바이트 수는?',answer,
            f'초당 채널당 표본 수×채널 수×표본당 바이트×초를 곱한다. {rate}×{channels}×({depth}÷8)×{seconds}={answer}바이트이다. 압축 형식의 비트율 계산과 구별한다.')
    a = family(3, 'scan-pixels', '균일 해상도 스캔의 화소 수', '픽셀')
    for i in range(20):
        width, height, dpi = 2+i%4, 3+i//4, 100
        answer = width*height*dpi*dpi
        add(a,[width,height,dpi],f'가로 {width}인치, 세로 {height}인치 영역을 가로·세로 모두 {dpi}dpi로 샘플링한다. 한 점을 한 픽셀로 저장하고 재표본화하지 않을 때 총 픽셀 수는?',answer,
            f'가로 픽셀은 {width}×{dpi}, 세로 픽셀은 {height}×{dpi}이다. 두 값을 곱하면 {width}×{height}×{dpi}²={answer}픽셀이다. 픽셀 수와 바이트 수는 색 깊이가 없으므로 동일시하지 않는다.')
    a = family(3, 'utf8-bytes', '정해진 UTF-8 문자의 데이터량', '바이트')
    for i in range(20):
        ascii_count, hangul_count = 12+i, 4+i%6
        answer = ascii_count+3*hangul_count
        add(a,[ascii_count,hangul_count],f'ASCII 범위 문자 {ascii_count}개와 완성형 한글 음절 문자 {hangul_count}개를 UTF-8로 저장한다. 각 한글은 U+AC00~U+D7A3의 한 코드 포인트이며 줄 바꿈·공백 추가·BOM은 없다. 총 바이트 수는?',answer,
            f'UTF-8에서 ASCII 범위 문자는 각각 1바이트, 지정 범위의 완성형 한글 음절은 각각 3바이트다. {ascii_count}×1+{hangul_count}×3={answer}바이트다. 분해된 자모나 결합 문자 등은 없는 조건이다.')
    a = family(3, 'byte-not', '8비트 단위 반전', '(10진수)')
    for i in range(20):
        value, bits = 20+7*i, 8
        digits = f'{value:08b}'
        inverted = ''.join('0' if bit=='1' else '1' for bit in digits)
        answer = sum(int(bit)*2**p for p,bit in enumerate(reversed(inverted)))
        add(a,[value,bits],f'부호 없는 8비트 값 {digits}(10진수 {value})의 각 비트를 0↔1로 반전한다. 반전 결과를 다시 부호 없는 10진수로 해석하면?',answer,
            f'{digits}의 각 비트를 반전하면 {inverted}이다. 이를 부호 없이 해석하면 {answer}이다. 8비트 범위에서 원래 값과 반전 값을 더하면 255이며 부호 있는 정수 해석이나 2의 보수와 구별한다.')
    assert len(FAMILIES) == 29
    assert all(len(f['items']) == 20 for f in FAMILIES)
    return FAMILIES


def generate_numeric(make_question):
    bank=[]
    for family_index, f in enumerate(definitions()):
        for i, item in enumerate(f['items']):
            value=item['result']
            distractors=[]
            step=Fraction(1,10) if f['precision'] else Fraction(1)
            for shift in [1,-1,2,-2,3,4]:
                candidate=value+shift*step
                if candidate >= 0 and candidate != value and candidate not in distractors:
                    distractors.append(candidate)
                if len(distractors)==3: break
            answer=(family_index+i)%4+1
            choices=distractors[:]
            choices.insert(answer-1,value)
            q=make_question(
                id=f'WP-N-{f["key"]}-{i+1:03}', subject=f['subject'], topic=f['title'],
                question=item['question'], choices=[f'{format_number(x)} {f["unit"]}' for x in choices],
                answer=answer, explanation=item['explanation'])
            q.update(difficulty='중',family=f'WP-{f["key"]}',calculation=dict(
                kind=f['key'], values=item['values'], result=int(value) if value.denominator==1 else float(value),
                unit=f['unit'], precision=f['precision']))
            q['reviewNote']='AI의 일반 지식으로 자체 작성한 계산 조건 변형. 동일 family 20조건 중 하나이며 독립 개념이나 기출이 아님. 명시된 단순화 가정·단위·식·정답 및 해설을 내부 검토하고 별도 TypeScript 경로로 재계산 검증. 외부 전문가 검수와 공식 출제기준 대조 미완료. 저장소 주소는 작성 위치이며 외부 정답 증빙이 아님.'
            bank.append(q)
    return bank
