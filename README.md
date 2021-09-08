# Tello_Marker_Python

# anaconda environment


conda create -n Tello_Marker_Python_env python=3.8

conda env list

# activate 가상환경 시작
mac/linux
conda activate Tello_Marker_Python_env

windows
activate Tello_Marker_Python_env

# deactivate 가상환경 종료
mac/linux
conda deactivate

windows
deactivate

# install module
conda install spyder

conda install -c conda-forge basemap


# 가상환경 내보내기 (export)
conda env export > Tello_Marker_Python_env.yaml

# .yaml 파일로 새로운 가상환경 만들기
conda env create -f Tello_Marker_Python_env.yaml

# 가상환경 리스트 출력
conda env list

# 가상환경 제거하기
conda env remove -n Tello_Marker_Python_env
