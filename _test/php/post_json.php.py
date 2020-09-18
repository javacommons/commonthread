import json
import requests

d = {'kanagawa': ['横浜', '相模原', '湘南', '鎌倉'],
     'saitama': ['所沢',
                 '狭山',
                 '川口',
                 '浦和',
                 '小手指',
                 '飯能'],
     'tokyo': ['品川', '五反田', '三軒茶屋', '四谷']}

response = requests.post(
    'http://freeware.php.xdomain.jp/02-json-post.php',
    json.dumps(d),
    headers={'Content-Type': 'application/json'})
print(response.text)

"""
<?php
// POSTされたJSON文字列を取り出し
$json = file_get_contents("php://input");

// JSON文字列をobjectに変換
//   ⇒ 第2引数をtrueにしないとハマるので注意
$contents = json_decode($json, true);

// デバッグ用にダンプ
var_dump($contents);
"""