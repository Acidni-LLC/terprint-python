var builder = DistributedApplication.CreateBuilder(args);

var apiService = builder.AddProject<Projects.Terprint_ApiService>("apiservice");

builder.AddProject<Projects.Terprint_3_Web>("webfrontend")
    .WithExternalHttpEndpoints()
    .WithReference(apiService);

builder.Build().Run();
