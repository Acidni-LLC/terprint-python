
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Projects;

using Microsoft.AspNetCore.Identity;
//using Terprint.Web.Data;

var builder = DistributedApplication.CreateBuilder(args);

var cache = builder.AddRedis("cache");

var apiService = builder.AddProject<Projects.Terprint_ApiService>("apiservice");

builder.AddProject<Projects.Terprint_Web>("webfrontend")
    .WithExternalHttpEndpoints()
    .WithReference(apiService);

//builder.Services.AddDbContext<TerprintWebContext>(options =>
  //  options.UseSqlServer(builder.Configuration.GetConnectionString("TerprintWebContext") ?? throw new InvalidOperationException("Connection string 'TerprintWebContext' not found.")));

builder.Build().Run();
