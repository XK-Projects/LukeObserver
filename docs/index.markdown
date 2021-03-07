---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: observer
---

给录萪选个时间:

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