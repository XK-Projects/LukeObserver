---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: observer
---

Datetime Picker:

<input class="flatpickr flatpickr-input" type="text" placeholder="Select Date.." data-id="datetime"
        readonly="readonly" id="dtpicker">

<table>
  <thead>
    <tr>
      <th>时间</th>
      <th>录播</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td id="rptime"></td>
      <td id="rplink"></td>
    </tr>
  </tbody>
</table>