import urllib.request
import argparse
import os

img_urls=['https://cdn-images.farfetch-contents.com/19/42/18/09/19421809_43255382_1000.jpg',
          'https://cdn-images.farfetch-contents.com/19/42/18/09/19421809_43254899_1000.jpg']

img_base_path="../images/"

def init_args():
    # execution:
    # python example.py --project_id 7 --project_name myproject --mode keyword --keyword ribbon
    parser = argparse.ArgumentParser(description="Argparse for example.py")

    parser.add_argument('--project_id', type=int, required=True)
    parser.add_argument('--project_name', type=str, required=True)
    parser.add_argument('--mode', type=str, required=True)
    parser.add_argument('--keyword', type=str, default=None)
    parser.add_argument('--tag',action=argparse.BooleanOptionalAction) #default= False
    return parser

if __name__=="__main__":
    parser=init_args()
    args=parser.parser_args()
    
    filepath=img_base_path + args.project_id+"_"+args.project_name+"/"
    os.makedirs(filepath,exist_ok=False)
    
    for idx,url in enumerate(img_urls):
        urllib.request.urlretrieve(url, filepath + f"{idx}.jpg")
        print(filepath + f"{idx}.jpg"+" saved")