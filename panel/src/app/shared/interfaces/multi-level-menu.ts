export interface MultiLevelMenu {
  label: string;
  icon?: string;
  hidden?: boolean;
  link?: string;
  items?: MultiLevelMenu[];
  permissions?: string | string[];
  permissionState?: string;
  externalRedirect?: boolean;
  hrefTargetType?: '_blank' | '_self' | '_parent' | '_top' | 'framename';
}