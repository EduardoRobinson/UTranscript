import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TabsPage } from './tabs.page';

const routes: Routes = [
  {
    path: '',
    component: TabsPage,
    children: [
      {
        path: 'criarResumo',
        loadChildren: () => import('../create/tab1.module').then(m => m.Tab1PageModule)
      },
      {
        path: 'listarVideoAulas',
        loadChildren: () => import('../read/tab2.module').then(m => m.Tab2PageModule)
      },
      {
        path: 'minhasVideoAulas',
        loadChildren: () => import('../readByUser/tab3.module').then(m => m.Tab3PageModule)
      },
      {
        path: 'configuracao',
        loadChildren: () => import('../userConfig/tab4.module').then(m => m.Tab4PageModule)
      },
      {
        path: 'youtubeDownloader',
        loadChildren: () => import('../youtubeDownloader/tab5.module').then(m => m.Tab5PageModule)
      },
      {
        path: 'videoaula/:id',
        loadChildren: () => import('../readById/read-by-id.module').then(m => m.ReadByIdPageModule)
      },
      {
        path: '',
        redirectTo: 'criarResumo',
        pathMatch: 'full'
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TabsPageRoutingModule {}