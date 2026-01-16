import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { IThemeManager } from '@jupyterlab/apputils';

/**
 * Initialization data for the jupyterlab_theme_melon extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_theme_melon:plugin',
  description: 'a dark theme for jupyterlab',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    console.log('JupyterLab extension jupyterlab_theme_melon is activated!');
    const style = 'jupyterlab_theme_melon/index.css';

    manager.register({
      name: 'jupyterlab_theme_melon',
      isLight: true,
      load: () => manager.loadCSS(style),
      unload: () => Promise.resolve(undefined)
    });
  }
};

export default plugin;
