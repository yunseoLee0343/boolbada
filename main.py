from sensors.person_detector import detect_person_from_camera

if detect_person_from_camera(show_preview=False):
    print("사람이 감지되었습니다.")
else:
    print("사람이 감지되지 않았습니다.")