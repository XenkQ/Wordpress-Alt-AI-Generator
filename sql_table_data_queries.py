class SQL_Table_Data_Queries:
    def __init__(self, tables_prefix: str):
        self.SELECT_IMAGE_IDS_LINKS_WITHOUT_ALT = f"""
        SELECT DISTINCT {tables_prefix}posts.ID, {tables_prefix}posts.guid
        FROM {tables_prefix}posts
        LEFT JOIN {tables_prefix}postmeta ON {tables_prefix}posts.ID = {tables_prefix}postmeta.post_id
        WHERE {tables_prefix}posts.post_mime_type REGEXP '^image/'
          AND {tables_prefix}posts.ID NOT IN (
            SELECT post_id
            FROM {tables_prefix}postmeta
            WHERE meta_key = '_wp_attachment_image_alt'
          );
        """

        self.SELECT_IMAGE_IDS_LINKS_WITH_EXISTING_EMPTY_ALT_ROW = f"""
        SELECT {tables_prefix}posts.id, {tables_prefix}posts.guid, {tables_prefix}postmeta.meta_value
        FROM {tables_prefix}posts INNER JOIN {tables_prefix}postmeta ON {tables_prefix}posts.ID = {tables_prefix}postmeta.post_id
        WHERE {tables_prefix}postmeta.meta_key = '_wp_attachment_image_alt' AND meta_value = '';
        """

        self.INSERT_IMAGE_ALT_DATA = f"""
        INSERT INTO {tables_prefix}postmeta (post_id, meta_key, meta_value) VALUE (%s, '_wp_attachment_image_alt', %s);
        """

        self.UPDATE_IMAGE_ALT_DATA = f"""
        UPDATE {tables_prefix}postmeta SET meta_value = %s WHERE meta_key = '_wp_attachment_image_alt' AND post_id = %s;
        """
