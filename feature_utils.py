import math

from core import BoundingBox


def get_iou(box_1: BoundingBox, box_2: BoundingBox):
    x_min = max(box_1.x_min, box_2.x_min)
    x_max = min(box_1.x_max, box_2.x_max)
    y_min = max(box_1.y_min, box_2.y_min)
    y_max = min(box_1.y_max, box_2.y_max)

    if x_max < x_min or y_max < y_min:
        return 0.0

    intersection_area = (x_max - x_min) * (y_max - y_min)
    union_area = box_1.get_area() + box_2.get_area() - intersection_area

    if union_area == 0.0:
        return 0.0

    iou = intersection_area / union_area
    assert 0.0 <= iou <= 1.0
    return iou


def get_euclidean_distance(box_1: BoundingBox, box_2: BoundingBox):
    return math.sqrt((box_1.x_center - box_2.x_center) ** 2.0 + (box_1.y_center - box_2.y_center) ** 2.0)


def get_intersection_area(box_1: BoundingBox, box_2: BoundingBox):
    x_min = max(box_1.x_min, box_2.x_min)
    x_max = min(box_1.x_max, box_2.x_max)
    y_min = max(box_1.y_min, box_2.y_min)
    y_max = min(box_1.y_max, box_2.y_max)
    if x_max < x_min or y_max < y_min:
        return 0.0
    intersection_area = (x_max - x_min) * (y_max - y_min)
    return intersection_area


def get_intersection_area_percentage(box_1: BoundingBox, box_2: BoundingBox):
    if box_1.get_area() == 0.0:
        return 0.0
    return get_intersection_area(box_1=box_1, box_2=box_2) / box_1.get_area()


def extract_box_features(box: BoundingBox):
    box_features = [
        box.x_min,
        box.y_min,
        box.x_max,
        box.y_max,
        box.x_max - box.x_min,
        box.y_max - box.y_min,
        box.x_center,
        box.y_center,
        box.get_area(),
    ]
    one_hot_encoding = [0] * 100
    one_hot_encoding[box.category] = 1
    box_features += one_hot_encoding
    return box_features


def extract_pairwise_features(box_1: BoundingBox, box_2: BoundingBox):
    return [
        box_1.x_min - box_2.x_min,
        box_1.y_min - box_2.y_min,
        box_1.x_max - box_2.x_max,
        box_1.y_max - box_2.y_max,
        box_1.x_center - box_2.x_center,
        abs(box_1.x_center - box_2.x_center),
        box_1.y_center - box_2.y_center,
        abs(box_1.y_center - box_2.y_center),
        get_iou(box_1, box_2),
        get_euclidean_distance(box_1, box_2),
        box_1.get_area() - box_2.get_area(),
        abs(box_1.get_area() - box_2.get_area()),
        get_intersection_area(box_1, box_2),
        get_intersection_area_percentage(box_1, box_2),
        get_intersection_area_percentage(box_2, box_1),
    ]
