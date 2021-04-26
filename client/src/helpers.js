export const normalizeStringDecimal = (stringDecimal) => {
    if (stringDecimal === 'None') {return '-'};
    return parseFloat(stringDecimal).toFixed(4);
}