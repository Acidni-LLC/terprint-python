using Terprint.components;
using Terprint.Web;
using Terprint.Web.Components;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
//using Terprint.Web.Data;
using Microsoft.AspNetCore.Identity;
using Terprint.Web.Data;

var builder = WebApplication.CreateBuilder(args);

// Add service defaults & Aspire components.
builder.AddServiceDefaults();

// Add services to the container.
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

builder.Services.AddRazorPages();
builder.Services.AddDbContext<TerprintWebContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("TerprintWebContext") ?? throw new InvalidOperationException("Connection string 'TerprintWebContext' not found.")));
builder.Services.AddDbContext<TerprintWebContext2>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("TerprintWebContext") ?? throw new InvalidOperationException("Connection string 'TerprintWebContext' not found.")));


builder.Services.AddQuickGridEntityFrameworkAdapter();;
builder.Services.AddOutputCache();
builder.Services.AddSingleton<Terprint.common.Components>();
builder.Services.AddSingleton<Terprint.Web.Components.Pages.BatchChooser>();
builder.Services.AddSingleton<Terprint.Web.Components.Pages.BatchPages.Create >();


builder.Services.AddHttpClient<WeatherApiClient>(client =>
    {
        // This URL uses "https+http://" to indicate HTTPS is preferred over HTTP.
        // Learn more about service discovery scheme resolution at https://aka.ms/dotnet/sdschemes.
        client.BaseAddress = new("https+http://apiservice");
    });

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();

app.UseStaticFiles();
app.UseAntiforgery();

app.UseOutputCache();

app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();



app.UseRouting();
app.UseAntiforgery();
app.MapRazorPages();

app.MapDefaultEndpoints();

app.Run();
