export default function processPlaces(placesWithDetails) {
  const placesThatExist = placesWithDetails
    .filter((place) => !!place)
    .map((place) => ({
      business_status: place.business_status,
      formatted_address : place.formatted_address,
      geometry: place.geometry,
      icon: place.icon,
      icon_background_color: place.icon_background_color,
      icon_mask_base_uri: place.icon_mask_base_uri,
      opening_hours: place.opening_hours,
      plus_code: place.plus_code,
      reference: place.reference,
      user_ratings_total: place.user_ratings_total,
      name: place.name,
      vicinity: place.vicinity,
      rating: place.rating,
      tag: place.types.join(", "),
      url: place.url,
      lat: place.geometry.location.lat,
      lng: place.geometry.location.lng,
      placeId: place.place_id,
      status: place.business_status,
      photo: place.photos,
    }));


  return placesThatExist;
}

// module.exports = processPlaces;
