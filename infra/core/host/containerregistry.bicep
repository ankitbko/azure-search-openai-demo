param name string
param location string = resourceGroup().location
param tags object = {}

resource acr 'Microsoft.ContainerRegistry/registries@2023-01-01-preview' = {
  name: name
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    adminUserEnabled: true
  }
  tags: tags
}

// output identityPrincipalId string = acr.identity.principalId
output name string = acr.name
output loginserver string = acr.properties.loginServer
