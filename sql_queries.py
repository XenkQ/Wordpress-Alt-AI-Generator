SELECT_IMAGE_IDS_LINKS_WITHOUT_ALT = """
SELECT DISTINCT nwqz_posts.ID, nwqz_posts.guid
FROM nwqz_posts
LEFT JOIN nwqz_postmeta ON nwqz_posts.ID = nwqz_postmeta.post_id
WHERE nwqz_posts.post_mime_type REGEXP '^image/'
  AND nwqz_posts.ID NOT IN (
    SELECT post_id
    FROM nwqz_postmeta
    WHERE meta_key = '_wp_attachment_image_alt'
  );
"""

SELECT_IMAGE_IDS_LINKS_WITH_EXISTING_EMPTY_ALT_ROW = """
SELECT nwqz_posts.id, nwqz_posts.guid, nwqz_postmeta.meta_value
FROM nwqz_posts INNER JOIN nwqz_postmeta ON nwqz_posts.ID = nwqz_postmeta.post_id
WHERE nwqz_postmeta.meta_key = '_wp_attachment_image_alt' AND meta_value = '';
"""

INSERT_IMAGE_ALT_DATA = """
INSERT INTO nwqz_postmeta (post_id, meta_key, meta_value) VALUE (%s, '_wp_attachment_image_alt', %s);
"""

UPDATE_IMAGE_ALT_DATA = """
UPDATE nwqz_postmeta SET meta_value = %s WHERE meta_key = '_wp_attachment_image_alt' AND post_id = %s;
"""