var overlayMaps = {}; // this controls the layers that appear in the map, this is variable and will be updated when the user 
var map; //global map
let heatmapLayer = null;
var is_heatmap_active = false;
var global_selected_layer;
var layerControl
var baseMaps


function getRandomColor() {
  let letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}


const originalStyles = {
  "Locations": {
    style: function (feature) {
      return {
        fillColor: "green",
        color: "green",
        weight: 2,
        opacity: 1,
        fillOpacity: 0.25
      };
    }
  },
  "Concelhos": {
    style: function (feature) {
      return {
        fillColor: "blue",
        color: "blue",
        weight: 2,
        opacity: 1,
        fillOpacity: 0.25
      };
    },
    onEachFeature: function (feature, layer) {
      layer.bindPopup(feature.properties.county_name + " - " + feature.properties.population);
    }
  },
  "Distritos": {
    style: function (feature) {
      return {
        fillColor: "red",
        color: "red",
        weight: 2,
        opacity: 1,
        fillOpacity: 0.1
      };
    },
    onEachFeature: function (feature, layer) {
      layer.bindPopup(feature.properties.nome);
    }
  }
};



function loadMap(raw_layers_objects, navbarContent) {
    // Inicialize o mapa com as coordenadas centralizadas em Portugal
    map = L.map('map', {
        center: [39.3999, -8.2245],
        zoom: 7,
        zoomControl: false // disable the default zoom control
      });
      
      L.control.zoom({
        position: 'bottomleft' // position the zoom control in the bottom left corner
      }).addTo(map);

  // Adicione uma camada de mapa base do Google Maps
  var googleMaps = L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
    maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
  });
  concelhos = raw_layers_objects.concelhos;
  distritos = raw_layers_objects.distritos;
  locations = raw_layers_objects.locations;

  // Adicione o layer GeoJSON com informações sobre os concelhos
  var locations_layer = L.geoJSON(locations, {
    style: function (feature) {
      return originalStyles["Locations"].style(feature);
    },
  })

  var concelhos_layer = L.geoJSON(concelhos, {
    // Defina o estilo do layer
    style: function (feature) {
      return originalStyles["Concelhos"].style(feature);
    },
    // Adicione um evento de clique ao layer para mostrar um popup com informações
    onEachFeature: function (feature, layer) {
      layer.bindPopup(feature.properties.county_name);
    }
  });

  // Adicione uma camada de satélite do Google Maps
  var googleSatellite = L.tileLayer('http://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
    maxZoom: 20,
    subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
  });

  concelhos = raw_layers_objects.concelhos;
  distritos = raw_layers_objects.distritos;
  locations = raw_layers_objects.locations;

  // Adicione o layer GeoJSON com informações sobre os concelhos
  var locations_layer = L.geoJSON(locations, {
    style: function (feature) {
      return originalStyles["Locations"].style(feature);
    },
  })


  var concelhos_layer = L.geoJSON(concelhos, {
    // Defina o estilo do layer
    style: function (feature) {
      return originalStyles["Concelhos"].style(feature);
    },
    // Adicione um evento de clique ao layer para mostrar um popup com informações
    onEachFeature: function (feature, layer) {
      layer.bindPopup(feature.properties.county_name);
    }
  });

  // Adicione o layer GeoJSON com informações sobre os concelhos
  var distritos_layer = L.geoJSON(distritos, {
    // Defina o estilo do layer
    style: function (feature) {
      return originalStyles["Distritos"].style(feature);
    },
    // Adicione um evento de clique ao layer para mostrar um popup com informações
    onEachFeature: function (feature, layer) {
      layer.bindPopup(feature.properties.nome);
    }
  });

  var areas_layer = L.geoJSON(areas, {
    // Defina o estilo do layer
    style: function (feature) {
      return {
        color: "green",
        weight: 2,
        opacity: 1,
        fillOpacity: 0.1
      };
    },
    // Adicione um evento de clique ao layer para mostrar um popup com informações
    onEachFeature: function (feature, layer) {

      var p_array = ""
      area_properties.forEach(element => {
        if (element['area_nome'] == feature.properties.nome) {
          p_array += '<div class="popup-property">' + element['nome'] + " " + element['value'] + '</div>';
        }
      });
      var popupContent = '<div class="custom-popup">' +
        '<h4>' + feature.properties.nome + '</h4>' +
        '<input type="text" id="search-input" placeholder="Search"> <br><br>' +
        '<div class="popup-content">' + p_array
        + '</div>' + '</div>';

      layer.bindPopup(popupContent);

      layer.on('popupopen', function () {
        var input = document.getElementById('search-input');
        input.addEventListener('input', function () {
          searchInPopup(input.value);
        });
      });

    }
  });


  // Crie um objeto com as camadas base disponíveis
  baseMaps = {
    "Mapa": googleMaps,
    "Satélite": googleSatellite
  };

  // Crie um objeto com as camadas de overlay disponíveis
  overlayMaps = {
    "Distritos": distritos_layer,
    "Concelhos": concelhos_layer,
    "Locations": locations_layer,
    "Areas": areas_layer,
  };



  // Searchable fields???



  // Adicione um controle de camadas ao mapa
  layerControl = L.control.layers(baseMaps, overlayMaps);
  layerControl.setPosition('bottomright');
  layerControl.addTo(map);

  // Adicione a camada de mapa base ao mapa
  googleMaps.addTo(map);

  // Adicione o layer de concelhos ao mapa
  concelhos_layer.addTo(map);

  // Adicione o layer de distritos ao mapa
  //distritos_layer.addTo(map);
  locations_layer.addTo(map);
  areas_layer.addTo(map);

  L.Control.Navbar = L.Control.extend({
    options: {
      position: 'topleft'
    },

    onAdd: function () {
      var container = L.DomUtil.create('div', '');

      container.innerHTML = navbarContent;

      return container;
    }
  });

  L.control.navbar = function (options) {
    return new L.Control.Navbar(options);
  };

  var navbarControl = L.control.navbar().addTo(map);


}

function open_heatmap_config_modal() {
  const modalBody = document.getElementById('heatmap-modal-config');

  // Limpa o modal body antes de adicionar novos elementos
  modalBody.innerHTML = '';

  // Itera sobre as chaves na variável global overlayMaps
  for (const [key, value] of Object.entries(overlayMaps)) {
    const layerName = document.createElement('h3');
    layerName.innerText = `${key}:`;
    modalBody.appendChild(layerName);

    const attributeList = document.createElement('ul');
    let attributeCount = 0;

    // Itera sobre as propriedades do primeiro objeto no GeoJSON
    if (!value.getLayers()[0]) {
      continue;
    }
    for (const prop in value.getLayers()[0].feature.properties) {
      const propValue = value.getLayers()[0].feature.properties[prop];

      // Verifica se o valor da propriedade é numérico ou uma string numérica
      if (typeof propValue === 'number' || !isNaN(parseFloat(propValue))) {
        const listItem = document.createElement('li');

        const label = document.createElement('label');
        label.innerText = prop;

        const radioButton = document.createElement('input');
        radioButton.type = 'radio';
        radioButton.name = `${key}-attribute`;
        radioButton.value = prop;
        radioButton.id = `${key}-${prop}`;

        label.prepend(radioButton);
        listItem.appendChild(label);
        attributeList.appendChild(listItem);
        attributeCount++;
      }
    }

    if (attributeCount > 0) {
      modalBody.appendChild(attributeList);
    } else {
      const noAttributesMsg = document.createElement('p');
      noAttributesMsg.innerText = 'Não existem atributos para esta camada';
      modalBody.appendChild(noAttributesMsg);
    }
  }

  // Adiciona evento de clique para ativar somente um botão de opção por vez
  const radioButtons = document.querySelectorAll('input[type="radio"]:not(.leaflet-control-layers-selector)');
  radioButtons.forEach(button => {
    button.addEventListener('click', () => {
      radioButtons.forEach(otherButton => {
        if (otherButton !== button) {
          otherButton.checked = false;
        }
      });
    });
  });


  // Chamar a função generate_heatmap quando o usuário selecionar um atributo
  document.querySelectorAll('#heatmap-modal-config input[type="radio"]:not(.leaflet-control-layers-selector)').forEach(button => {
    button.addEventListener('click', generate_heatmap);
  });





  // Mostra o modal
  $('#heatmap-modal').modal('show');
}

function searchInPopup(searchText) {
  // Perform your search logic within the popup
  console.log();
  var contentElement = document.querySelector('.popup-content');
  var lines = contentElement.getElementsByClassName('popup-property');
  var visibleLines = 0;
  for (var i = 0; i < lines.length; i++) {
    var lineText = lines[i].innerText;
    if (lineText.includes(searchText)) {
      lines[i].style.display = 'block';
      visibleLines++;
    } else {
      lines[i].style.display = 'none';
    }
  }
}


// Definir uma função para colorir os polígonos com base no valor do atributo selecionado
// Definir a função de preenchimento de cor
function getFillColor(value, quartiles) {
  return value > quartiles[2] ? 'red' :
    value > quartiles[1] ? 'yellow' :
      value > quartiles[0] ? 'lime' :
        'blue';
}

function getHeatmapStyle(value, quartiles) {
  return {
    fillColor: getFillColor(value, quartiles),
    fillOpacity: 0.7,
    weight: 1,
    opacity: 1,
    color: 'white'
  }
}



function get_quartiles_for_heatmap(values) {
  // Ordenar os valores e calcular os quartis
  values.sort((a, b) => a - b);
  let quartiles = [
    values[Math.round(values.length * 0.25)],
    values[Math.round(values.length * 0.5)],
    values[Math.round(values.length * 0.75)]
  ];

  return quartiles;
}


function generate_heatmap() {
  console.log("generate_heatmap")
  // Obter o valor do atributo selecionado
  const selectedAttribute = document.querySelector('input[type="radio"]:not(.leaflet-control-layers-selector):checked').value;

  // Obter a camada selecionada
  const selectedLayer = overlayMaps[document.querySelector('input[type="radio"]:not(.leaflet-control-layers-selector):checked').name.replace('-attribute', '')];

  global_selected_layer = selectedLayer;

  if (!selectedLayer) {
    is_heatmap_active = false;
    document.getElementById("remove-heatmap").style.display = "none";
    return;
  }
  is_heatmap_active = true;
  document.getElementById("remove-heatmap").style.display = "block";

  // Obter todos os valores presentes nos dados
  let values = [];
  selectedLayer.eachLayer(function (layer) {
    if (layer.feature && layer.feature.properties[selectedAttribute]) {
      values.push(parseFloat(layer.feature.properties[selectedAttribute]));
    }
  });



  quartiles = get_quartiles_for_heatmap(values);

  // Definir a função de estilo para aplicar as cores aos polígonos
  function style(feature) {
    let value = parseFloat(feature.properties[selectedAttribute]);
    value = parseFloat(value.toFixed(2));
    return getHeatmapStyle(value, quartiles);
  }

  // Aplicar o estilo aos polígonos na camada selecionada
  selectedLayer.setStyle(style);
}









function remove_heatmap() {
  is_heatmap_active = false;
  for (const [layerName, layer] of Object.entries(overlayMaps)) {

    if (originalStyles[layerName]) {
      layer.setStyle(originalStyles[layerName].style);
    } else {
      layer.setStyle({
        fillColor: getRandomColor(),
        color: getRandomColor(),
        fillOpacity: 0.7,
        weight: 2,
        opacity: 1,
      });
    }

  }

  document.getElementById("remove-heatmap").style.display = "none";
}






window.addEventListener('load', function () {
  // Crie uma referência para o elemento de entrada de pesquisa
  const searchInput = document.getElementById("map-search");

  // Armazene as camadas que foram removidas durante a pesquisa
  const removedLayers = new Map();

  searchInput.addEventListener("keyup", function (event) {
    let searchValue = event.target.value;


    removedLayers.forEach((layerName, layer) => {

      overlayMaps[layerName].addLayer(layer);
      removedLayers.delete(layer);
    });


    // Continue com a lógica de pesquisa atual
    for (const [key, value] of Object.entries(overlayMaps)) {
      let layers = value.getLayers();

      for (const layer of layers) {
        let matchFound = false;

        for (const prop in layer.feature.properties) {
          if (prop === "geometry_type") {
            continue;
          }

          let new_prop = "" + layer.feature.properties[prop];

          if (new_prop.toLowerCase().includes(searchValue.toLowerCase())) {
            matchFound = true;
            break;
          }
        }

        if (matchFound) {
          // Se a camada foi removida anteriormente, adicione-a novamente
          if (removedLayers.has(layer)) {
            value.addLayer(layer);
            removedLayers.delete(layer);
          }


          // Se o heatmap estiver ativo, aplique os estilos de heatmap
          if (is_heatmap_active && global_selected_layer === value) {

            selectedLayer = value;
            selectedAttribute = document.querySelector('input[type="radio"]:not(.leaflet-control-layers-selector):checked').value;
            // Obter todos os valores presentes nos dados
            let values = [];
            selectedLayer.eachLayer(function (layer) {
              if (layer.feature && layer.feature.properties[selectedAttribute]) {
                values.push(parseFloat(layer.feature.properties[selectedAttribute]));
              }
            });



            quartiles = get_quartiles_for_heatmap(values);

            // Definir a função de estilo para aplicar as cores aos polígonos
            function style(feature) {
              let value = parseFloat(feature.properties[selectedAttribute]);
              value = parseFloat(value.toFixed(2));
              return getHeatmapStyle(value, quartiles);
            }

            // Aplicar o estilo aos polígonos na camada selecionada
            selectedLayer.setStyle(style);


          }

        } else {
          // Se a camada não foi removida antes, remova-a e armazene-a no removedLayers
          if (!removedLayers.has(layer)) {
            value.removeLayer(layer);
            removedLayers.set(layer, key);
          }
        }
      }
    }

  });




  // cria um objeto modal usando Bootstrap
  let importModal = new bootstrap.Modal(document.getElementById('importModal'), {});

  document.getElementById('import-file').addEventListener('click', function () {
    document.getElementById('fill-color').value = getRandomColor();
    document.getElementById('border-color').value = getRandomColor();
    importModal.show();
  });

  let reader = new FileReader();
  let iscsv = false;
  let layerName
  let fillColor
  let borderColor
  let fillOpacity
  let weight

  reader.onload = function (e) {
    let geojson
    if (iscsv) {
      const contents = e.target.result;
      const jsonData = csv_to_json(contents);

      file = jsonData;
      geojson = JSON.parse(jsonData);
    } else {
      geojson = JSON.parse(event.target.result);
    }

    let importedLayer = L.geoJSON(geojson, {
      style: function (feature) {
        return {
          fillColor: fillColor,
          color: borderColor,
          fillOpacity: fillOpacity,
          weight: weight
        };
      },
      onEachFeature: function (feature, layer) {
        if (fileproperties != null) {
          p_array = "";
          propertiesData = JSON.parse(fileproperties);
          for (let p of propertiesData['Area_list']) {
            if (p["name"] == feature.properties.name) {
              for (let key in p["Properties"]) {
                p_array += '<div class="popup-property">' + key + " " + p["Properties"][key] + '</div>';
              }
            }
          }
          var popupContent = '<div class="custom-popup">' +
            '<h4>' + feature.properties.name + '</h4>' +
            '<input type="text" id="search-input" placeholder="Search"> <br><br>' +
            '<div class="popup-content">' + p_array
            + '</div>' + '</div>';

          layer.bindPopup(popupContent);

          layer.on('popupopen', function () {
            var input = document.getElementById('search-input');
            input.addEventListener('input', function () {
              searchInPopup(input.value);
            });
          });
        } else layer.bindPopup(feature.properties.name);
      }
    }).addTo(map).bindTooltip(layerName);


    // Adiciona o layer ao objeto overlayMaps
    overlayMaps[layerName] = importedLayer;

    // Atualiza o controle de layers para incluir o novo layer
    map.removeControl(layerControl);
    layerControl = L.control.layers(baseMaps, overlayMaps);
    layerControl.setPosition('bottomright');
    layerControl.addTo(map);


  }


  document.getElementById('import-button').addEventListener('click', async function () {
    let fileInputcsv = document.getElementById('file-upload-csv');
    let fileInputjson = document.getElementById('file-upload-json');
    let fileProperties = document.getElementById('file-upload-properties');
    let file;

    layerName = document.getElementById('layer-name').value || file.name;
    fillColor = document.getElementById('fill-color').value || getRandomColor();
    borderColor = document.getElementById('border-color').value;
    fillOpacity = document.getElementById('fill-opacity').value || 1;
    weight = document.getElementById('weight').value || 2;

    if (fileProperties.files[0] != null) {
      let propertiesFile = fileProperties.files[0];
      const promise = new Promise((resolve, reject) => {
        let reader2 = new FileReader();

        reader2.onload = function (e) {
          const contents = e.target.result;
          fileproperties = csv_to_json_properties(contents); 
          resolve(reader2.result)
        };
        reader2.onerror = reject;
        reader2.readAsText(propertiesFile);
      });
      await promise;
    }


    if (fileInputjson.files[0] == null && fileInputcsv.files[0] != null) {
      iscsv = true;
      let scvFile = fileInputcsv.files[0];
      reader.readAsText(scvFile);

    } else {
      iscsv = false;
      let jsonfile;
      jsonfile = fileInputjson.files[0];
      reader.readAsText(jsonfile);
    }

    // clear the input
    fileInputcsv.value = '';
    fileInputjson.value = '';
    fileProperties.value = '';
  }
  );





  document.getElementById("heatmap-btn").addEventListener("click", open_heatmap_config_modal);
  document.getElementById("remove-heatmap").addEventListener("click", remove_heatmap);
});
let fileproperties;
function csv_to_json(csv) {

  var lines = csv.split("\n");

  var result = {};
  result['type'] = "FeatureCollection";
  features = [];

  var headers = lines[0].split(";");
  let geometryHeader;
  let nameHeader;
  for (let j = 0; j < headers.length; j++) {
    if (headers[j].trim() == 'geometry') {
      geometryHeader = j;
    }
    if (headers[j].trim() == 'sccode') {
      nameHeader = j;
    }
  }
  for (var i = 1; i < lines.length; i++) {
    const line = lines[i].split(';')
    var dict = {};
    dict['type'] = "Feature";
    dict["geometry"] = {};
    if (line[geometryHeader] != undefined) {
      let geometryString = line[geometryHeader].split(',');
      let geometry = [];
      let type = "";
      let multipolygon = [];
      let polygon = false;

      for (let s of geometryString) {
        if (s[0] == 'P') {
          type = "Polygon";
          polygon = true;
          let s2 = s.split('(');
          let s3 = s2[2].split(' ');
          let c1 = parseFloat(s3[0]);
          let c2 = parseFloat(s3[1]);
          geometry.push([c1, c2]);
        } else if (s[0] == 'M') {
          type = "MultiPolygon"
          let s2 = s.split('(');
          let s3 = s2[3].split(' ');
          let c1 = parseFloat(s3[0]);
          let c2 = parseFloat(s3[1]);
          multipolygon.push([c1, c2]);
        } else {
          if (polygon) {
            let c1;
            let c2;
            if (s[s.length - 1] == ')') {
              let s2 = s.split(' ')
              c1 = parseFloat(s2[1])
              let s3 = s2[2].split(')')
              c2 = parseFloat(s3[0])
            } else {
              let s2 = s.split(' ')
              c1 = parseFloat(s2[1])
              c2 = parseFloat(s2[2])
            }
            geometry.push([c1, c2])
          } else {
            if ((s[s.length - 1]) == ')') {
              let s2 = s.split(' ')
              let s3 = s2[2].split(')')
              let c1 = parseFloat(s2[1])
              let c2 = parseFloat(s3[0])
              multipolygon.push([c1, c2])
              geometry.push(multipolygon)
              multipolygon = []
            } else if (s[1] == '(') {
              let s2 = s.split(' ')
              let s3 = s2[1].split('(')
              let c1 = parseFloat(s3[2])
              let c2 = parseFloat(s2[2])
              multipolygon.push([c1, c2])
            } else {
              let s2 = s.split(' ')
              let c1 = parseFloat(s2[1])
              let c2 = parseFloat(s2[2])
              multipolygon.push([c1, c2])
            }
          }
        }

      }
      dict["geometry"]["type"] = type
      dict["geometry"]["coordinates"] = [geometry]
      dict["properties"] = {}

      if (fileproperties != null) {
        propertiesData = JSON.parse(fileproperties);
        for (let p of propertiesData['Area_list']) {
          if (p["name"] == line[nameHeader]) {
            dict["properties"] = p["Properties"]
          }
        }
      }
      dict["properties"]["name"] = line[nameHeader];
      features.push(dict);
    }
  }
  result['features'] = features;
  return JSON.stringify(result); //JSON
}

function csv_to_json_properties(csv) {
  var lines = csv.split("\n");
  var headers = lines[0].split(",");
  let nameHeader;
  for (let j = 0; j < headers.length; j++) {
    if (headers[j].trim() == 'sccode') {
      nameHeader = j;
    }
  }
  data = {}
  data["type"] = "Area_list";
  data["Area_list"] = [];


  for (var i = 1; i < lines.length; i++) {
    const line = lines[i].split(',')
    dict = {}
    dict["name"] = line[nameHeader]
    dict["Properties"] = {}
    for (var j = 0; j < headers.length; j++) {
      if (j != nameHeader) {
        dict["Properties"][headers[j]] = line[j];
      }
    }


    data["Area_list"].push(dict)
  }
  return JSON.stringify(data);
}


/*

  1.

*/