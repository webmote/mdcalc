export function unitConvert (unit, value, convert) {
  var cv = convert[unit]
  if (cv && value) {
    cv = cv.replace('value', value)
    var val = eval(cv)
    console.debug(unit, cv, '=', val)
    return val
  } else {
    console.warn(unit, cv, value)
  }
}
