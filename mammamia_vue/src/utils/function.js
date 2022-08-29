// kalkulasi jarak
export function calculate(a,b) {
    return a + Math.round(b);
}
// membuat random Kode bayar
export function kd_bayar(length) {
    var result = '';
    for ( var i = 0; i < length; i++ ) {
        result += Math.floor(Math.random() * 100)+1;
    }
    return result;
}
// membuat randomChar
export function randomChar(length) {
    var result           = '';
    var characters       = '123456789';
    var charactersLength = characters.length;
    for ( var i = 0; i < length; i++ ) {
        result += characters.charAt(Math.floor(Math.random() * 
        charactersLength));
   }
   return result;
}
// format harga
export function formatPrice(value) {
    let val = (value/1).toFixed(0).replace('.', ',')
    return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")
}