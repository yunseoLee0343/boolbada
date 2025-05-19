from picamera2 import Picamera2
import cv2

def detect_person_from_camera(show_preview=False):
    # HOG 기반 사람 감지기 초기화
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # Picamera2 초기화
    import pdb;pdb.set_trace()
    picam2 = Picamera2()
    picam2.configure(picam2.create_still_configuration())

    # 카메라 시작
    picam2.start()

    person_detected = False

    print("[INFO] 사람 감지를 시작합니다. Ctrl+C로 종료하세요.")

    try:
        while True:
            # 카메라로부터 프레임 읽기
            frame = picam2.capture_array()

            # 프레임에서 사람 감지
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            boxes, _ = hog.detectMultiScale(gray, winStride=(8,8))

            if len(boxes) > 0:
                print("[INFO] 사람 감지됨!")
                person_detected = True
                break  # 한 번만 감지되면 종료

            if show_preview:
                # 감지 영역 표시 (디버깅용)
                for (x, y, w, h) in boxes:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.imshow('Person Detection', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    except KeyboardInterrupt:
        print("[INFO] 중단됨.")

    finally:
        picam2.stop()
        if show_preview:
            cv2.destroyAllWindows()

    return person_detected