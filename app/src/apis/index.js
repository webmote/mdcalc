import request from '@/utils/request'

export function getInfoSs (ssKey) {
  return request({
    url: '/content/ss/' + ssKey,
    method: 'GET'
  }).then(function (res) {
    return Promise.resolve(res)
  })
}

export function getHotSs () {
  return request({
    url: '/content/ss',
    method: 'GET'
  })
}

export function getSs () {
  return request({
    url: '/content/ss',
    method: 'GET'
  })
}
