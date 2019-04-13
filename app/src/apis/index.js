import request from '@/utils/request'

export function getInfoSs (ssKey) {
  return request({
    url: '/content/ss/' + ssKey,
    method: 'GET'
  }).then(function (res) {
    return Promise.resolve(res)
  })
}

export function getHotSs (kw) {
  return request({
    url: '/content/ss?kw=' + (kw || ''),
    method: 'GET'
  })
}

export function getSs (kw) {
  return request({
    url: '/content/ss?kw=' + (kw || ''),
    method: 'GET'
  })
}
