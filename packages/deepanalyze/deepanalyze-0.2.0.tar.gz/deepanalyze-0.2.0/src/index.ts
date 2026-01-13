import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { ILauncher } from '@jupyterlab/launcher';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { IDefaultFileBrowser } from '@jupyterlab/filebrowser';

import { openDeepAnalyze, restoreDeepAnalyzeIfNeeded } from './deepanalyze/open';
import { installScratchCellRewriteUI } from './deepanalyze/scratchCellRewrite';

/**
 * deepanalyze 插件入口。
 *
 * 说明：
 * - 在 Launcher 注册 “DeepAnalyze” 按钮，点击后创建/打开工作区与布局。
 * - 在 `app.restored` 后尝试恢复上一次的 DeepAnalyze 会话（基于 localStorage 中记录的 workspace 信息）。
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'deepanalyze:plugin',
  description: 'DeepAnalyze JupyterLab Extension',
  autoStart: true,
  requires: [ILauncher, IDocumentManager, IDefaultFileBrowser],
  activate: (
    app: JupyterFrontEnd,
    launcher: ILauncher,
    docManager: IDocumentManager,
    defaultBrowser: IDefaultFileBrowser
  ) => {
    const command = 'deepanalyze:open';
    app.commands.addCommand(command, {
      label: 'DeepAnalyze',
      caption: '打开 DeepAnalyze 工作区与布局',
      iconClass: 'deepanalyze-launcher-icon',
      iconLabel: 'DeepAnalyze',
      execute: () => openDeepAnalyze(app, docManager, defaultBrowser)
    });

    launcher.add({
      command,
      category: 'Other',
      rank: 50
    });

    // 全局：所有 notebook 单元格右键“使用大模型编辑”
    installScratchCellRewriteUI(app);

    void app.restored.then(async () => {
      await restoreDeepAnalyzeIfNeeded(app, docManager, defaultBrowser);
    });
  }
};

export default plugin;
