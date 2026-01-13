// @ts-nocheck
import { browser } from 'fumadocs-mdx/runtime/browser';
import type * as Config from '../source.config';

const create = browser<typeof Config, import("fumadocs-mdx/runtime/types").InternalTypeConfig & {
  DocData: {
  }
}>();
const browserCollections = {
  docs: create.doc("docs", {"api_reference.md": () => import("../content/docs/api_reference.md?collection=docs"), "integrations.md": () => import("../content/docs/integrations.md?collection=docs"), "mcp_architecture.md": () => import("../content/docs/mcp_architecture.md?collection=docs"), "observability.md": () => import("../content/docs/observability.md?collection=docs"), "quickstart.md": () => import("../content/docs/quickstart.md?collection=docs"), }),
};
export default browserCollections;