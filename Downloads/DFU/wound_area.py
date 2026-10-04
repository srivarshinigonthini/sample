import cv2
import numpy as np

def calculate_wound_area(image):
    """
    Detect wound region and calculate ulcer area percentage.
    """

    img = cv2.resize(image, (224, 224))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold to detect darker ulcer regions
    _, thresh = cv2.threshold(
        blur,
        110,
        255,
        cv2.THRESH_BINARY_INV
    )

    kernel = np.ones((3, 3), np.uint8)

    thresh = cv2.morphologyEx(
        thresh,
        cv2.MORPH_OPEN,
        kernel
    )

    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    output = img.copy()

    total_area = img.shape[0] * img.shape[1]
    ulcer_area = 0

    for cnt in contours:

        area = cv2.contourArea(cnt)

        if area > 80:

            ulcer_area += area

            cv2.drawContours(
                output,
                [cnt],
                -1,
                (0, 255, 0),
                2
            )

    percent = (ulcer_area / total_area) * 100

    return output, percent