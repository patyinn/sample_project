# sample project api

## 啟用:

在 docker-compose.yml資料夾上，下`docker-compose up`指令，即可啟用，會自動建立一位可進行編輯的使用者。

* 帳號: `superuser`
* 密碼: `superpassword`

## djangorestframework-simplejwt 處理JWT驗證:

1. 取得token，設定一小時內有效。
    * url pattern: http://127.0.0.1:8082/api/token/
    * method: POST
    * payload:
         ```
         { 
              "uesrname": 使用者名稱,
              "password": 使用者密碼,
         }
         ```
    * response:
         ```
         {
              "refresh": 更新token,
              "access": token
         }
         ```
2. 更新token:
    * url pattern: http://127.0.0.1:8082/api/token/refresh/
    * method: POST
    * payload:
         ```
         { 
              "refresh": 更新token,
         }
         ```
    * response:
         ```
         {
              "refresh": 更新token,
              "access": token
         }
         ```

## 熱門文章endpoint:

### 前置作業:

從djangorestframework-simplejwt的endpoint取得的access，放入操作文章endpoint的header中，使用Bearer token。

例如:
`'Authorization': f'Bearer {access}',` 在python requests模組的header中。

### 熱門文章操作:

1. 取得以文章日期為排序的全部有效文章:
    * url pattern: http://127.0.0.1:8082/hot/
    * method: GET
    * response:
    ```
    [
        {
            "id": 文章編號,
            "date": 文章日期,
            "title": 標題,
            "content": 內容,
            "cover": 封面照片網址位置,
            "picture": 內部照片網址位置,
            "url": 文章頁面連結,
            "valid": 是否有效,
            "user": 使用者名稱,
            "latest_edit_date": 最後更新日期
        },
        ...
    ]
    ```
2. 建立熱門文章，以及在其之下的排行文章:
    * [NOTE1] 熱門文章id會以`f'{使用日期}HOT{最新一筆文章+1}'`自動產生，排行文章id則是`f'{熱門文章id}_{排名}'`
      ，無法指定、編輯以及變更。
    * [NOTE2] ranks傳送的方式須以list中包含每個排名文章的json物件方式傳送。
    * url pattern: http://127.0.0.1:8082/hot/
    * method: POST
    * payload:
      ```
         {
             "date": 文章日期(str, format:"%Y-%m-%d"),
             "title": 標題(str),
             "content": 內容(str),
             "cover": 封面照片檔案(image file),
             "picture": 內部照片檔案(image file),
             "url": 文章頁面連結(url),
             "ranks": [
                 {
                     "rank": 排名(int),
                     "title": 排名文章標題(str),
                     "content": 排名文章內容(str),
                     "pic": 以base64 encode的圖片檔(str),
                     "pic_name": 圖片檔的名稱(str),
                     "url": 延伸閱讀連結(url),
                     "url_title": 延伸閱讀名稱(str),
                 },
                 ...
             ],
             "valid": 是否有效(bool),
         }
      ```
    * response:
      ```
        {
             "id": 文章編號,
             "date": 文章日期,
             "title": 標題,
             "content": 內容,
             "cover": 封面照片網址位置,
             "picture": 內部照片網址位置,
             "url": 文章頁面連結,
             "rank_lsit": [
                 {
                     "rank_id": 排名文章編號,
                     "rank": 排名,
                     "title": 排名文章標題,
                     "content": 排名文章內容,
                     "pic": 圖片檔網址位置,
                     "url": 延伸閱讀連結,
                     "url_title": 延伸閱讀名稱,
                 },
                 ...
             ],
             "valid": 是否有效,
             "user": 使用者名稱,
             "latest_edit_date": 最後更新日期
        }
        ```

### 熱門文章單一項目操作:

1. 取得單一熱門文章的全部詳細資訊:
    * url pattern: http://127.0.0.1:8082/hot/{hot_article_id}/
    * method: GET
    * response:
    ```
    {
        "id": 文章編號,
        "date": 文章日期,
        "title": 標題,
        "content": 內容,
        "cover": 封面照片網址位置,
        "picture": 內部照片網址位置,
        "url": 文章頁面連結,
        "rank_lsit": [
            {
                "rank_id": 排名文章編號,
                "rank": 排名,
                "title": 排名文章標題,
                "content": 排名文章內容,
                "pic": 圖片檔網址位置,
                "url": 延伸閱讀連結,
                "url_title": 延伸閱讀名稱,
            },
            ...
        ],
        "valid": 是否有效,
        "user": 使用者名稱,
        "latest_edit_date": 最後更新日期
    }
    ```
2. 建立熱門文章之下的排行文章:
    * [NOTE1] 熱門文章id會以`f'{使用日期}HOT{最新一筆文章+1}'`自動產生，排行文章id則是`f'{熱門文章id}_{排名}'`
      ，無法指定、編輯以及變更。
    * [NOTE2] ranks傳送的方式須以list中包含每個排名文章的json物件方式傳送。
    * [NOTE3] 需要有此id的熱門文章，並且此endpoint只能用來新增排名文章，無法變更熱門文章、排名文章。
    * url pattern: http://127.0.0.1:8082/hot/{hot_article_id}/
    * method: POST
    * payload:
      ```
         {
             "ranks": [
                 {
                     "rank": 排名(int),
                     "title": 排名文章標題(str),
                     "content": 排名文章內容(str),
                     "pic": 以base64 encode的圖片檔(str),
                     "pic_name": 圖片檔的名稱(str),
                     "url": 延伸閱讀連結(url),
                     "url_title": 延伸閱讀名稱(str),
                 },
                 ...
             ],
         }
      ```
        * response:
          ```
          {
               "id": 文章編號,
               "date": 文章日期,
               "title": 標題,
               "content": 內容,
               "cover": 封面照片網址位置,
               "picture": 內部照片網址位置,
               "url": 文章頁面連結,
               "rank_lsit": [
                   {
                       "rank_id": 排名文章編號,
                       "rank": 排名,
                       "title": 排名文章標題,
                       "content": 排名文章內容,
                       "pic": 圖片檔網址位置,
                       "url": 延伸閱讀連結,
                       "url_title": 延伸閱讀名稱,
                   },
                   ...
               ],
               "valid": 是否有效,
               "user": 使用者名稱,
               "latest_edit_date": 最後更新日期
          }
          ``` 
3. 更新熱門文章以及排行文章:
    * [NOTE1] 熱門文章id、排名文章id、日期以及排名無法變更。
    * [NOTE2] ranks傳送的方式須以list中包含每個排名文章的json物件方式傳送。
    * [NOTE3] 需要有此id的熱門文章，並且此endpoint只能用來新增排名文章，無法變更熱門文章、排名文章。
    * url pattern: http://127.0.0.1:8082/hot/{hot_article_id}/
    * method: PUT
    * payload:
      ```
         {
             "date": 文章日期(str, format:"%Y-%m-%d"),
             "title": 標題(str),
             "content": 內容(str),
             "cover": 封面照片檔案(image file),
             "picture": 內部照片檔案(image file),
             "url": 文章頁面連結(url),
             "ranks": [
                 {
                     "rank": 排名(int),
                     "title": 排名文章標題(str),
                     "content": 排名文章內容(str),
                     "pic": 以base64 encode的圖片檔(str),
                     "pic_name": 圖片檔的名稱(str),
                     "url": 延伸閱讀連結(url),
                     "url_title": 延伸閱讀名稱(str),
                 },
                 ...
             ],
             "valid": 是否有效(bool),
         }
      ```
        * response:
          ```
          {
               "id": 文章編號,
               "date": 文章日期,
               "title": 標題,
               "content": 內容,
               "cover": 封面照片網址位置,
               "picture": 內部照片網址位置,
               "url": 文章頁面連結,
               "rank_lsit": [
                   {
                       "rank_id": 排名文章編號,
                       "rank": 排名,
                       "title": 排名文章標題,
                       "content": 排名文章內容,
                       "pic": 圖片檔網址位置,
                       "url": 延伸閱讀連結,
                       "url_title": 延伸閱讀名稱,
                   },
                   ...
               ],
               "valid": 是否有效,
               "user": 使用者名稱,
               "latest_edit_date": 最後更新日期
          }
          ``` 
4. 刪除熱門文章以及排行文章:
    * url pattern: http://127.0.0.1:8082/hot/{hot_article_id}/
    * method: DELETE
    * response:
   ```
    {
         "message": f"delete entry: {self.product_obj14.pk} successfully"
    }
    ```