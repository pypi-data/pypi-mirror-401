from setuptools import setup, find_packages

setup(
    name='kolabpy',
    version='1.0.4.1',  # 업데이트할 버전
    description='Contributor:te.park@snu.ac.kr,kkd8326@snu.ac.kr',
    author='Kyungdong Kim', # 관리자님 성함 또는 이메일
    author_email='kkd8326@snu.ac.kr',
    packages=find_packages(), # 현재 폴더의 패키지들을 자동으로 찾음
    install_requires=[
        'saspy',
        'requests',
        'pandas',
        'geopandas',
        'folium',
        'ipython',
        'pygments',
        'beautifulsoup4',  # bs4 import를 위해 필요
    ],
    python_requires='>=3.6', # f-string 등이 사용되었으므로 3.6 이상 권장
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License', # 라이선스에 맞게 수정
        'Operating System :: OS Independent',
    ],
)