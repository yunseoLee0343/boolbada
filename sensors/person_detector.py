import cv2

def detect_person_from_camera(show_preview=False):
    # HOG 기반 사람 감지기 초기화
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # 카메라 열기 (0번은 기본 웹캠)
    cap = cv2.VideoCapture(0)

    person_detected = False

    if not cap.isOpened():
        print("[ERROR] 카메라를 열 수 없습니다.")
        return False

    print("[INFO] 사람 감지를 시작합니다. Ctrl+C로 종료하세요.")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("[ERROR] 프레임을 읽을 수 없습니다.")
                break

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
        cap.release()
        if show_preview:
            cv2.destroyAllWindows()

    return person_detected