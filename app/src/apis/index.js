import request from '@/utils/request'

export function getInfoSs (ssKey) {
  return request({
    url: '/content/ss/' + ssKey,
    method: 'GET'
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
