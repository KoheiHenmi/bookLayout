#coding:utf-8
import sys
import json
import cv2

def process_bb_box(json_path,image_path):
    with open(json_path,encoding="utf-8_sig") as f:
        bb_json = json.load(f)
        bb_json['img'] = image_path
        return bb_json

def search_pathes(json_dir,file_type):
    file_pathes = []
    if os.path.exists(json_dir):
        files = os.listdir(dir)
        for file_path in files:
            if file_path.split('.')[-1] == file_type:
                file_pathes.extend([file_path])
    else:
        print("Don't exist",json_dir)
    return file_pathes
    
def read_json_list(json_dir,image_dir):
    json_pathes = search_pathes(json_dir,'json')
    image_pathes = search_pathes(image_dir,'JPG')
    assert len(json_pathes) == len(image_pathes)

    json_pathes.sort()
    image_pathes.sort()

    return [process_bb_box(json_path,image_path) for json_path,image_path in zip(json_pathes,image_pathes)]


def recursive_parse_example_to_dict(example):
  """Recursively parses XML contents to python dict.

  We assume that `object` tags are the only ones that can appear
  multiple times at the same level of a tree.

  Args:
    xml: xml tree obtained by parsing XML file contents using lxml.etree

  Returns:
    Python dictionary holding XML contents.
  """
    result = {}
    for key,value in example.items():
        if key == 'labels':
            result['object'] = []
            for label in example[key]:
                result['object'] = {}# ['bndbox'] = {}
                result['object']['bndbox'] = \
                {'xmin':value['box2d']['x1'],
                'ymin':value['box2d']['y1'],
                'xmax':value['box2d']['x2'],
                'ymax':value['box2d']['y2']}
                result['object']['name'] = value['category']
        elif key == 'img':
            # 画像の縦横pixel数を取得→sizeに入れる
            result['size'] = {}
            img = cv2.imread(value,cv2.IMREAD_COLOR)
            result['size']['width'] = img.shape[:3][1]
            result['size']['height'] = img.shape[:3][0]

            # filenameに入れる
            img_name = value.split('/')[-1]
            result['filename'] = img_name

    return result

        #result[key].append()

  """
  result = {}
  for child in example:
    child_result = recursive_parse_xml_to_dict(child)
    if child.tag != 'object':
      result[child.tag] = child_result[child.tag]
    else:
      if child.tag not in result:
        result[child.tag] = []
      result[child.tag].append(child_result[child.tag])
  return {xml.tag: result}
  """

if __name__ == "__main__":
    #pass
    #url = r"C:\data\train_annotations\train_annotations\train_764167_0045.json"
    #print(process_bb_box(url))