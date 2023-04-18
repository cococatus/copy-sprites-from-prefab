from unityparser import UnityDocument
import pathlib
import itertools
import shutil


PREFABS_PATH = "prefabs"
SPRITES_PATH = 'sprites'
OUTPUT_PATH = 'used_sprites'

all_guids = set()


def get_guids():
    # get prefab yaml
    for prefab in pathlib.Path(PREFABS_PATH).glob("**/*.prefab"):
        print(prefab.name)
        doc = UnityDocument.load_yaml(prefab)
        sprites = doc.filter(class_names=('MonoBehaviour', 'SpriteRenderer'), attributes=('m_Sprite',))
        # get all spites guids from prefab
        guids_in_prefab = {sprite.m_Sprite.get('guid') for sprite in sprites if sprite.m_Sprite.get('guid') is not None}
        all_guids.update(guids_in_prefab)

    guids = list(all_guids)
    guids.sort()
    # for g in guids:
    #     print(g)


# go through metas and copy files with used guids to folder
# if file exists override it
def copy_sprites():
    texture_path = pathlib.Path(SPRITES_PATH)
    for meta in itertools.chain(texture_path.glob("**/*.png.meta"), texture_path.glob("**/*.jpg.meta")):
        guid = _get_guid_meta(meta)
        if guid in all_guids:
            shutil.copy2(meta, OUTPUT_PATH)
            file = pathlib.PurePath(meta).with_suffix("")
            shutil.copy2(file, OUTPUT_PATH)
        # print(f"{meta.name} guid: {guid}")


# credit https://developers.10antz.co.jp/archives/1030
def _get_guid_meta(meta):
    with open(meta) as f:
        for line in f.read().splitlines():
            label = "guid: "
            if line.startswith(label):
                guid = line.replace(label, "")
                return guid
        return None


if __name__ == '__main__':
    get_guids()
    copy_sprites()
