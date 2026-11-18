/* Explicit per-reviewer storage. No reads are performed on page creation. */
(function(root){
 'use strict';
 function create(storage,packageId,fingerprint,policyHash,groupIds){
  function reviewer(id){if(typeof id!=='string'||!id.trim()||id!==id.trim())throw Error('请填写不含首尾空白的审核者编号');return id}
  function key(id){return ['KDIR-review-v2',packageId,fingerprint,reviewer(id)].map(encodeURIComponent).join(':')}
  function validate(data,id){
   if(!data||data.reviewer_anonymous_id!==reviewer(id)||data.package_id!==packageId||data.package_fingerprint!==fingerprint||data.policy_sha256!==policyHash||data.stage!==1)throw Error('审核者、资料版本或政策不匹配');
   if(!Array.isArray(data.groups)||data.groups.length!==groupIds.length||new Set(data.groups.map(g=>g.group_id)).size!==groupIds.length||!data.groups.every(g=>groupIds.includes(g.group_id)))throw Error('审核组不匹配');
   return data;
  }
  return {save(id,data){validate(data,id);storage.setItem(key(id),JSON.stringify(data))},load(id){const raw=storage.getItem(key(id));return raw===null?null:validate(JSON.parse(raw),id)},clear(id){storage.removeItem(key(id))},validate,key};
 }
 const api={create};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.ReviewStorage=api;
})(typeof globalThis!=='undefined'?globalThis:this);
