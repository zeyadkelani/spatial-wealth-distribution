import { Client } from"@googlemaps/google-maps-services-js";
import { existsSync, mkdirSync } from "fs";
import ProgressBar from "progress";
import { Parser } from"json2csv";
import fs from'fs';
import config from"./config.json" assert { type: "json" };
import { getGrid, sleep } from "./helpers.js";
import processPlaces from"./processPlaces.js";
const client = new Client({});

const locationsFile = fs.readFileSync('../../Processing Codes/boundaries_interest.json');
const {locations} = JSON.parse(locationsFile);

const numIterations = locations.length;

async function getNearby(
  searchRadiusInMeters,
  places,
  latLongPoint,
  pagetoken
) {
  if (pagetoken) {
    await sleep(2000);
  }
  const response = await client
    .placesNearby({
      params: {
        key: config.apiKey,
        keyword: config.searchTerm,
        radius: searchRadiusInMeters,
        location: latLongPoint,
        language: config.language,
        pagetoken,
      },
    })
    .catch((e) => {
      console.log(e);
    });
  if (response.data.next_page_token) {
    return getNearby(
      searchRadiusInMeters,
      places.concat(response.data.results),
      latLongPoint,
      response.data.next_page_token
    );
  } else {
    return places.concat(response.data.results);
  }
}

async function getAllPlaces(latLongPoint, searchRadiusInMeters, grid, count) {
  console.log("getting places from: ", latLongPoint, " ", searchRadiusInMeters);
  const placesFromGoogle = await getNearby(
    searchRadiusInMeters,
    [],
    latLongPoint
  );
  if (placesFromGoogle.length === 60) {
    const subGrib = getGrid(
      [latLongPoint[0] - grid.latStep, latLongPoint[0] + grid.latStep],
      [latLongPoint[1] - grid.longStep, latLongPoint[1] + grid.longStep],
      searchRadiusInMeters / 4
    );
    const morePlaces = await traverse(subGrib, searchRadiusInMeters / 4, null, count + 1);
    return morePlaces;
  }
  return placesFromGoogle;
}

async function traverse(grid, searchRadiusInMeters, bar, count) {
  if(count === 2){
    console.log("Limit Exceeded!");
    return [];
  }
  let places = [];
  console.log("grid steps: ", grid.steps.length);
  for (let i = 0; i < grid.steps.length; i++) {
    if (bar) bar.tick();
    const gridSectionPlaces = await getAllPlaces(
      grid.steps[i],
      searchRadiusInMeters,
      grid,
      count
    );
    places = places.concat(gridSectionPlaces);
  }
  return places;
}

export async function run() {
  
  for (let i = 0; i < numIterations; i++) {
    const location = locations[i];
    config.latRange[0] = location.lat_range[0];
    config.latRange[1] = location.lat_range[1];
    config.longRange[0] = location.long_range[0];
    config.longRange[1] = location.long_range[1];
    
    fs.writeFileSync('config.json', JSON.stringify(config));
    const grid = getGrid(
      config.latRange,
      config.longRange,
      config.searchRadiusInMeters
    );

    console.log(`Starting transversal of grid...`);
    const bar = new ProgressBar("[:bar] :percent :etas", {
      total: grid.steps.length,
    });
    const places = await traverse(grid, config.searchRadiusInMeters, bar, 0);

    const { placesWithDetails } = places.reduce((res, place) => {
      if (!res.placeIds.includes(place.place_id)) {
        return {
          placeIds: res.placeIds.concat(place.place_id),
          placesWithDetails: res.placesWithDetails.concat(place),
        };
      }

      return res;
    }, { placeIds: [], placesWithDetails: [] });

    console.log(`Grid transversal complete...`);

    console.log(
      `discovered ${places.length} ${config.searchTerm}s, of which ${placesWithDetails.length} are unique`
    );
    
    const outputFolder = `out/output_${location.ADM2}_poi_${config.searchTerm}`;

    const processedPlaces = processPlaces(placesWithDetails);
    if (!existsSync(outputFolder)) {
      mkdirSync(outputFolder);
    }
    
    // Write the rawPlaceList.json file
    fs.writeFileSync(`${outputFolder}/rawPlaceList.json`, JSON.stringify({ places }, null, 2));
    
    // Write the placesWithDetails.json file
    fs.writeFileSync(`${outputFolder}/placesWithDetails.json`, JSON.stringify({ places: placesWithDetails }, null, 2));
    
    // Write the sortedPlaces.json file
    fs.writeFileSync(`${outputFolder}/sortedPlaces.json`, JSON.stringify({ places: processedPlaces }, null, 2));
    
    // Create a new instance of the Parser from json2csv
    const parser = new Parser();
    
    // Convert processedPlaces to CSV format
    const csv = parser.parse(processedPlaces);

  //   execSync('node index.js');

    // Rename the output folder
    //const oldFolderName = `output_${config.latitude[0]}_${config.longitude[0]}_${config.searchRadius}`;
    
    // Write the sortedPlaces.csv file
    fs.writeFileSync(`${outputFolder}/sortedPlaces.csv`, csv);
  }
}


run();