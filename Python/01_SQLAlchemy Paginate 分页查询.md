SQLAlchemy Paginate 分页查询



## 方法

```
db.session.query(User).filter_by().paginate(page=None, per_page=None,
    error_out=True, max_per_page=None)
```

参数定义：

- `page` 查询的页数

- `per_page` 每页的条数

- `max_per_page` 每页最大条数，有值时，`per_page` 受它影响

- ```
  error_out
  ```

   

  当值为 True 时，下列情况会报错

  - 当 page 为 1 时，找不到任何数据
  - page 小于 1，或者 per_page 为负数
  - page 或 per_page 不是整数

该方法返回一个分页对象 `Pagination`

## Pagination

调用 `paginate()` 方法，会返回一个 `Pagination` 对象，它封装了当前页的各种数据和方法，具体如下

### 字段

- `has_next` 如果下一页存在，返回 True

- `has_prev` 如果上一页存在，返回 True

- `items` 当前页的数据列表

- `next_num` 下一页的页码

- `page` 当前页码

- `pages` 总页数

- `per_page` 每页的条数

- `prev_num` 上一页的页码

- `query` 用于创建此分页对象的无限查询对象。

- `total` 总条数

- `iter_pages(left_edge=2, left_current=2, right_current=5, right_edge=2)`
  迭代分页中的页码，四个参数，分别控制了省略号左右两侧各显示多少页码，在模板中可以这样渲染

  ```
  {% macro render_pagination(pagination, endpoint) %}
    <div class=pagination>
    {% for page in pagination.iter_pages() %}
      {% if page %}
        {% if page != pagination.page %}
          <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
        {% else %}
          <strong>{{ page }}</strong>
        {% endif %}
      {% else %}
        <span class=ellipsis>…</span>
      {% endif %}
    {%- endfor %}
    </div>
  {% endmacro %}
  ```

- `next(error_out=False)` 返回下一页的分页对象

- `prev(error_out=False)` 返回上一页的分页对象