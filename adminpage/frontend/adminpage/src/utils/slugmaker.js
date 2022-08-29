export function makeSlug (cName) {
    var slug = "";
    var titleLower = cName.toLowerCase();
    slug = titleLower.replace(/\s*$/g, '');
    slug = slug.replace(/\s+/g, '-');
    
    return slug;
}
export function formatPrice(value) {
    let val = (value/1).toFixed(0).replace('.', ',')
    return val.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".")
}