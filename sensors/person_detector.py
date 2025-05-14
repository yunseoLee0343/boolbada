import cv2
import picamera
import picamera.array

def detect_person_from_camera(show_preview=False):
    # HOG 기반 사람 감지기 초기화
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    # PiCamera 초기화
    with picamera.PiCamera() as camera:
        camera.resolution = (640, 480)  # 해상도 설정
        camera.framerate = 30           # 프레임 레이트 설정

        # PiCamera로부터 이미지 스트림 받기
        with picamera.array.PiRGBArray(camera) as output:
            person_detected = False

            print("[INFO] 사람 감지를 시작합니다. Ctrl+C로 종료하세요.")

            try:
                for frame in camera.capture_continuous(output, format="bgr", use_video_port=True):
                    # 프레임 얻기
                    image = frame.array

                    # 프레임에서 사람 감지
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    boxes, _ = hog.detectMultiScale(gray, winStride=(8,8))

                    if len(boxes) > 0:
                        print("[INFO] 사람 감지됨!")
                        person_detected = True
                        break  # 한 번만 감지되면 종료

                    if show_preview:
                        # 감지 영역 표시 (디버깅용)
                        for (x, y, w, h) in boxes:
                            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                        cv2.imshow('Person Detection', image)

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

                    # 프레임 버퍼 비우기
                    output.truncate(0)
            
            except KeyboardInterrupt:
                print("[INFO] 중단됨.")

            finally:
                if show_preview:
                    cv2.destroyAllWindows()

    return person_detected
