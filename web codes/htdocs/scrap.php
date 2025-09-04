<?php
// رابط JSON
$url = 'https://script.googleusercontent.com/macros/echo?user_content_key=wplNr1PHKKbEFCsT_n2BAK8sl7dn2uxCdcey10EFYvVZP3RtfJsd_b8pvFv-A_Ks5JixT1V9kftoeKAD978_3ZU9M-n2qLa1m5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnIuAuShvbzNYIdD63NIMN3tRfUvrgp3iNwlHDB5i67AQX7ltp68wNPY72ZxrHmeFZoXO0cTm9vwN4nPdI1noU18XsGgtLOP6cNz9Jw9Md8uu&lib=MbPXKUtV_kIfccyq8QcAMo1AsrUbCW4ru';
// old url:'https://script.googleusercontent.com/macros/echo?user_content_key=utnJBmUPYyLb136fqxIbC9dV1LIyDzNxn4mJOU7PoDdrSPZwZxoug8qmh_bGQjOPM-MJjUBrgx36WJBRvshenSXyJ2sQ2M9nm5_BxDlH2jW0nuo2oDemN9CCS2h10ox_1xSncGQajx_ryfhECjZEnLuVJ7nIuQQ7aqRa4TRRSEdaSOnKfhNgA8DScBGsuQHw3bFjh_iGOouWC5SxyrOY8caM8CV3FIyfoCit_GtNGUe0weD80hDY_tz9Jw9Md8uu&lib=MbPXKUtV_kIfccyq8QcAMo1AsrUbCW4ru'
$json_data = file_get_contents($url);

if ($json_data === false) {
    die('فشل في جلب البيانات من الرابط.');
}

$file_path = 'data.json';
if (file_put_contents($file_path, $json_data)) {
    echo "تم حفظ البيانات بنجاح في الملف: $file_path";
} else {
    echo "فشل في حفظ البيانات.";
}
?>
