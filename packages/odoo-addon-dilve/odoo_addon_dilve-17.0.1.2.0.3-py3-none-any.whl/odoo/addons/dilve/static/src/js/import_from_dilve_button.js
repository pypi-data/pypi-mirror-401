/** @odoo-module **/
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
const { Component } = owl;
const cogMenuRegistry = registry.category("cogMenu");

export class CogMenu extends Component {
    setup() {
        this.actionService = useService("action");
    }

    async actionImportFromDilve() {
        try {
            this.actionService.doAction("dilve.dilve_import_products_step1_action");
        } catch (error) {
            console.error("Error al abrir el wizard:", error);
        }
    }
}
CogMenu.template = "blog_cog_menu.ImportFromDilve";
CogMenu.components = { DropdownItem };

export const CogMenuItem = {
    Component: CogMenu,
    groupNumber: 20,
    isDisplayed: ({ searchModel }) => {
        return searchModel.resModel === 'product.template';
    },
};

cogMenuRegistry.add("import-from-dilve", CogMenuItem, { sequence: 10 });