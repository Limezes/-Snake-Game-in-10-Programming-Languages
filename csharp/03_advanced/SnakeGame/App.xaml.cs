using System.Windows;
using Microsoft.Extensions.DependencyInjection;
using SnakeGame.Services;
using SnakeGame.ViewModels;

namespace SnakeGame
{
    public partial class App : Application
    {
        private readonly ServiceProvider _serviceProvider;

        public App()
        {
            var services = new ServiceCollection();
            ConfigureServices(services);
            _serviceProvider = services.BuildServiceProvider();
        }

        private void ConfigureServices(IServiceCollection services)
        {
            services.AddSingleton<IDatabaseService, DatabaseService>();
            services.AddSingleton<ISoundService, SoundService>();
            services.AddSingleton<ISettingsService, SettingsService>();
            
            services.AddTransient<MainViewModel>();
            services.AddTransient<GameViewModel>();
            services.AddTransient<SettingsViewModel>();
            
            services.AddSingleton<MainWindow>();
        }

        protected override void OnStartup(StartupEventArgs e)
        {
            base.OnStartup(e);

            var mainWindow = _serviceProvider.GetRequiredService<MainWindow>();
            var mainViewModel = _serviceProvider.GetRequiredService<MainViewModel>();
            
            mainWindow.DataContext = mainViewModel;
            mainWindow.Show();
        }
    }
}
