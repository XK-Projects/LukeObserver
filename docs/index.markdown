---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: observer
---

# 录萪观测者

你想什么时候去看录萪?

<input class="flatpickr flatpickr-input" type="text" placeholder="看录萪的时间..." data-id="datetime"
        readonly="readonly" id="dtpicker">

<table>
  <thead>
    <tr>
      <th>时间</th>
      <th>录萪在放...</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td id="rptime"></td>
      <td id="rplink"></td>
    </tr>
  </tbody>
</table>

# 轮播列表

<table>
  <thead>
    <tr>
      <th>轮播序号</th>
      <th>时长</th>
      <th>视频</th>
    </tr>
  </thead>
  <tbody id="video_row">
  </tbody>
</table>