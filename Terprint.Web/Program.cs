using Terprint.components;
using Terprint.Web;
using Terprint.Web.Components;
using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Components.Authorization;
using Microsoft.Extensions.DependencyInjection;
//using Terprint.Web.Data;
using Microsoft.AspNetCore.Identity;
using Terprint.Web.Data;
using Terprint.Web.Components.Account;
using Microsoft.AspNetCore.Components.Web;
using Blazored.LocalStorage;
using Aspire.Hosting.Redis;
using Microsoft.AspNetCore.Identity.UI.Services;
using Terprint.Web.Services;
using Microsoft.Identity.Web;

var builder = WebApplication.CreateBuilder(args);

// Add service defaults & Aspire components.
builder.AddServiceDefaults();

// Add services to the container.
builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents()
    .AddInteractiveWebAssemblyComponents();

builder.AddRedisClient("cache");
//builder.AddRedis("cache");
//builder.Services.AddStackExchangeRedisCache(options =>
//{
//    options.Configuration = "localhost:6000"; // Your Redis server connection string
//    options.InstanceName = "myApp"; // Optional: Prefix for cache keys
//});
 

builder.Services.AddCascadingAuthenticationState();
builder.Services.AddScoped<IdentityUserAccessor>();
builder.Services.AddScoped<IdentityRedirectManager>();
builder.Services.AddScoped<AuthenticationStateProvider, PersistingRevalidatingAuthenticationStateProvider>();

builder.Services.AddAuthentication(options =>
{
    options.DefaultScheme = IdentityConstants.ApplicationScheme;
    options.DefaultSignInScheme = IdentityConstants.ExternalScheme;
})
    .AddIdentityCookies();

builder.Services.AddAuthentication()
    .AddOpenIdConnect("Microsoft", "Microsoft", options =>
    {
        options.Authority = "https://login.microsoftonline.com/3278dcb1-0a18-42e7-8acf-d3b5f8ae33cd";
        options.ClientId = "de9598fc-7ece-4da1-8df7-20d9b4f9ad81";
        options.ClientSecret = "icJ8Q~1Zl9upHqQsXNYyJ_Oxaz1GYyTjklNnbaAl";
        options.ResponseType = "code";
        options.SaveTokens = true;
        options.CallbackPath = "/signin-oidc";
        options.SignInScheme = IdentityConstants.ExternalScheme;
    });

builder.Services.Configure<CookiePolicyOptions>(options =>
{
    options.CheckConsentNeeded = context => true;
    options.MinimumSameSitePolicy = SameSiteMode.None;
});
builder.Services.AddHttpContextAccessor();
builder.Services.AddScoped<HttpContextAccessor>();

builder.Services.AddRazorPages();

builder.Services.AddDbContext<TerprintWebContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("TerprintWebContext") ?? throw new InvalidOperationException("Connection string 'TerprintWebContext' not found.")));
builder.Services.AddDbContext<TerprintWebContext2>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("TerprintWebContext") ?? throw new InvalidOperationException("Connection string 'TerprintWebContext' not found.")));
builder.Services.AddDbContext<TerprintWebContext3>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("TerprintWebContext") ?? throw new InvalidOperationException("Connection string 'TerprintWebContext' not found.")));
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("TerprintWebContext") ?? throw new InvalidOperationException("Connection string 'TerprintWebContext' not found.")));

builder.Services.AddDatabaseDeveloperPageExceptionFilter();

builder.Services.AddIdentityCore<ApplicationUser>(options => options.SignIn.RequireConfirmedAccount = false)
    .AddEntityFrameworkStores<ApplicationDbContext>()
    .AddSignInManager()
    .AddDefaultTokenProviders();

builder.Services.AddTransient<IEmailSender, EmailSender>();

builder.Services.AddSingleton<IEmailSender<ApplicationUser>, IdentityNoOpEmailSender>();
builder.Services.AddQuickGridEntityFrameworkAdapter();;
builder.Services.AddOutputCache();
builder.Services.AddSingleton<Terprint.Web.common>();
builder.Services.AddSingleton<Terprint.Web.common.Components>();  
builder.Services.AddSingleton<Terprint.Web.common.AppState>();
builder.Services.AddSingleton<Terprint.Web.common.AppState.StateContainer.Rating>();
builder.Services.AddSingleton<Terprint.Web.common.AppState.StateContainer.RatingCategory>();
builder.Services.AddSingleton<Terprint.Web.common.AppState.StateContainer.Grower>();
builder.Services.AddSingleton<Terprint.Web.common.AppState.StateContainer.Batch>();
builder.Services.AddSingleton<Terprint.Web.common.AppState.StateContainer.Strain>();
builder.Services.AddSingleton<Terprint.Web.common.AppState.StateContainer.THCValue>();
builder.Services.AddSingleton<Terprint.Web.common.AppState.StateContainer.TerpeneValue>();
builder.Services.AddSingleton<Terprint.Web.Components.TerprintTable>();
builder.Services.AddSingleton<Terprint.Web.Components.ChooserBatch>();
builder.Services.AddSingleton<Terprint.Web.Components.ChooserRatingCategory>();
builder.Services.AddSingleton<Terprint.Web.Components.Pages.BatchPages.Create >();

builder.Services.AddBlazorBootstrap();

builder.Services.AddHttpClient<WeatherApiClient>(client =>
    {
        // This URL uses "https+http://" to indicate HTTPS is preferred over HTTP.
        // Learn more about service discovery scheme resolution at https://aka.ms/dotnet/sdschemes.
        client.BaseAddress = new("https+http://apiservice");
    });

builder.Services.AddScoped<AuthenticationStateProvider, IdentityRevalidatingAuthenticationStateProvider>();
builder.Services.AddScoped<AuthService>();

// Redis cache registration and cache service
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration.GetValue<string>("Redis:Configuration") ?? "localhost:6379";
    options.InstanceName = "Terprint:";
});

builder.Services.AddScoped<ICacheService, RedisCacheService>();

// register AuthService
builder.Services.AddScoped<Terprint.Web.Services.AuthService>();


var app = builder.Build();

app.MapDefaultEndpoints();

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
    .AddInteractiveServerRenderMode()
    .AddInteractiveWebAssemblyRenderMode();


app.UseCookiePolicy();

app.UseRouting();
app.UseAuthorization();
app.UseAntiforgery();
app.MapRazorPages();

app.MapDefaultEndpoints();

app.MapAdditionalIdentityEndpoints();

app.Run();
