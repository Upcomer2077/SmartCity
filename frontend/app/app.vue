<template>
  <div style="height:100vh; width:100vw">
    <LMap
      ref="map"
      :zoom="zoom"
      :center="centerOfView"
      :use-global-leaflet="false"
    >
      <LTileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution="<a href=&quot;https://www.openstreetmap.org/&quot;>OpenStreetMap</a> contributors"
        layer-type="base"
        name="OpenStreetMap"
      />
       <LCircle v-on:click="onclick"
    :lat-lng="[47.21322, -1.559482]"
    :radius="4500"
    :color="'red'"
  />
    </LMap>
  </div>
</template>

<script setup>
const zoom = ref(6)
const onclick=ref((e)=>{console.log("clicked",e)
 centerOfView.value =[ e?.latlng?.lat,e?.latlng?.lng]
  zoom.value=10
})
const centerOfView = ref([47.21322, -1.559482])
</script>