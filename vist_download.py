import json
import requests
from requests.adapters import HTTPAdapter, Retry
import glob, os, time, shutil


def download_image(id, url):
    fileType = url.split(".")[-1]
    with open(f'img/{id}.{fileType}', 'wb') as handle:
        try:
            # response = requests.get(url, stream=True)
            s = requests.Session()
            retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])
            s.mount('https://', HTTPAdapter(max_retries=retries))

            response = s.get(url, stream=True)
            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
        except Exception as e:
            print(f"Error {e} on {id}, {url}")


def get_downloaded_image_id(dirPath, ext=False):
    downloaded = set()
    for file in os.listdir(dirPath):
        if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".gif"):
            if ext:
                downloaded.add(file.split("."))
            else:
                downloaded.add(file.split(".")[0])
    return downloaded


def download_dataset():
    downloaded = get_downloaded_image_id('./img')
    dtypes = ['test', 'val', 'train']
    start = time.time()
    for dtype in dtypes:
        start_local = time.time()
        download_count = 0
        lst = [0]
        print(dtype)
        with open(f"./sis/filtered.{dtype}.story-in-sequence.json", 'r') as handle:
            data = json.load(handle)

        for images in data['images']:
            url = 'url_o' if 'url_o' in images else 'url_m'
            if images['id'] not in downloaded:
                download_image(images['id'], images[url])
                download_count += 1
            if download_count % 2000 == 0 and download_count not in lst:
                lst.append(download_count)
                print(f"  Downloaded {download_count} images in {dtype} so far in {time.time() - start_local} seconds")
        print(f"Downloaded {download_count}/{len(data['images'])} images in {time.time() - start_local} seconds.")
    
    print(f"Total time: {time.time() - start}")



def filter_broken_images():
    dtypes = ['test', 'val', 'train']
    broken_image_set = set()
    for dtype in dtypes:
        print(dtype)
        start = time.time()
        with open(f"./sis/{dtype}.story-in-sequence.json", 'r') as handle:
            data = json.load(handle)

        counts = {}
        image_url = {}
        new_images = []
        broken_images = 0
        total_images = len(data['images'])
        for image in data['images']:
            url = 'url_o' if 'url_o' in image else 'url_m'
            response = requests.head(image[url])
            if response.status_code == 200:
                ii = image[url].split(".")
                image_url[image['id']] = image[url]
                new_images.append(image)

                if ii[-1] in counts:
                    counts[ii[-1]] += 1
                else:
                    counts[ii[-1]] = 1
            else:
                broken_image_set.add(image['id'])
                broken_images += 1
        print(f'Filtered for broken images, elapsed time {time.time() - start}')
        print(counts)
        print(f'Images {broken_images}/{total_images}, {broken_images/total_images}% broken')
        stories = {}
        annotations = data['annotations']
        for annotation in annotations:
            story_id = annotation[0]['story_id']
            stories[story_id] = stories.get(story_id, []) + [annotation[0]]
        
        filtered_annotation = []
        good_images = set()
        broken_story_sequence = 0
        total_story_sequence = len(list(stories.keys()))
        for story_id, story_sequence in stories.items():
            storylet_complete = True
            for storylet in story_sequence:
                if storylet['photo_flickr_id'] in broken_image_set:
                    storylet_complete = False
                    broken_story_sequence += 1
                    break
                
            if storylet_complete:
                filtered_annotation += story_sequence
        print(f'Filtered for broken stories, elapsed time {time.time() - start}')
        print(f'Stories {broken_story_sequence}/{total_story_sequence}, \
            {broken_story_sequence/total_story_sequence}% broken')

        data['images'] = new_images
        data['annotations'] = filtered_annotation
        with open(f"./sis/filtered.{dtype}.story-in-sequence.json", 'w') as handle:
            json.dump(data, handle, ensure_ascii=False)

def sort_images():
    images = get_downloaded_image_id("./img")
    dtypes = ['val', 'test', 'train']
    for dtype in dtypes:
        print(dtype)
        start = time.time()
        with open(f"./sis/filtered.{dtype}.story-in-sequence.json", 'r') as handle:
            data = json.load(handle)
        counts = {}
        image_file = {}
        new_images = []
        broken_images = 0
        total_images = len(data['images'])
        for image in data['images']:
            url = 'url_o' if 'url_o' in image else 'url_m'
            ii = image[url].split(".")
            image_file[image['id']] = f"{image['id']}.{ii[-1]}"

        stories = {}
        annotations = data['annotations']
        unique_images = set()
        unique_stories = set()
        for annotation in annotations:
            # story_id = annotation['story_id']
            # stories[story_id] = stories.get(story_id, []) + [annotation]
            shutil.copy2(f"./img/{image_file[annotation['photo_flickr_id']]}", 
                    f"./img/{dtype}/{image_file[annotation['photo_flickr_id']]}")
            unique_images.add(annotation['photo_flickr_id'])
            unique_stories.add(annotation['story_id'])
        print(len(list(unique_images)), len(list(unique_stories)))
        
        # for story_id, story_sequence in stories.items():
        #     storylet_complete = True
        #     for storylet in story_sequence:
        #         shutil.copy2(f"./img/{image_file[storylet['photo_flickr_id']]}", 
        #             f"./img/{dtype}/{image_file[storylet['photo_flickr_id']]}")


def main():
    #filter_broken_images()
    #download_dataset()
    #sort_images()
    with open(f"./sis/filtered.val.story-in-sequence.json", 'r') as handle:
        data = json.load(handle)
    data['annotations'] = data['annotations'][:50]
    print(data['annotations'])
    image_file = {}
    for image in data['images']:
        url = 'url_o' if 'url_o' in image else 'url_m'
        ii = image[url].split(".")
        image_file[image['id']] = f"{image['id']}.{ii[-1]}"
    id = {}
    for annotation in data['annotations']:
        # story_id = annotation['story_id']
        # stories[story_id] = stories.get(story_id, []) + [annotation]
        if annotation['photo_flickr_id'] in id:
            id[annotation['photo_flickr_id']] += 1
        else:
            id[annotation['photo_flickr_id']] = 1
        shutil.copy2(f"./img/val/{image_file[annotation['photo_flickr_id']]}", 
                f"./chan-img/{image_file[annotation['photo_flickr_id']]}")
    with open(f"./sis/chan.val.story-in-sequence.json", 'w') as handle:
        json.dump(data, handle, ensure_ascii=False)

    print(id)
if __name__ == '__main__':
    main()